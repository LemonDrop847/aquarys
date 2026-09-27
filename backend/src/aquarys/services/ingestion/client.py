"""Resilient OAH Ingestion Client with retry, backoff, hashing, and raw payload persistence."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from aquarys.core.config import settings
from aquarys.core.logging import logger

RAW_DATA_DIR = Path(__file__).parents[3] / "data" / "raw"


class OAHClient:
    """Client for fetching data from OneAquaHealth API with resilience and provenance tracking."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: float = 15.0,
        raw_storage_dir: Optional[Path] = None,
    ) -> None:
        self.base_url = (base_url or settings.OAH_BASE_URL).rstrip("/")
        self.api_key = api_key or settings.OAH_API_KEY
        self.timeout = timeout_seconds
        self.raw_dir = raw_storage_dir or RAW_DATA_DIR
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    @property
    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    @staticmethod
    def compute_hash(payload: Any) -> str:
        """Computes SHA-256 hash of payload."""
        if isinstance(payload, (dict, list)):
            raw_bytes = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        elif isinstance(payload, str):
            raw_bytes = payload.encode("utf-8")
        elif isinstance(payload, bytes):
            raw_bytes = payload
        else:
            raw_bytes = str(payload).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()

    def _persist_raw_payload(self, endpoint: str, data: Any, payload_hash: str) -> Path:
        """Saves raw API response to disk with timestamp and hash."""
        sanitized_endpoint = endpoint.strip("/").replace("/", "_")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"{sanitized_endpoint}_{timestamp}_{payload_hash[:8]}.json"
        target_path = self.raw_dir / filename
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "endpoint": endpoint,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "payload_hash": payload_hash,
                    "data": data,
                },
                f,
                indent=2,
            )
        return target_path

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def fetch_endpoint(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetches a single endpoint with exponential backoff."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("Fetching OAH endpoint: %s with params %s", url, params)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self._headers, params=params)
            response.raise_for_status()
            data = response.json()

            payload_hash = self.compute_hash(data)
            self._persist_raw_payload(endpoint, data, payload_hash)

            return {
                "endpoint": endpoint,
                "data": data,
                "payload_hash": payload_hash,
                "retrieved_at": datetime.now(timezone.utc),
            }

    async def fetch_paginated(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_pages: int = 5,
        page_size: int = 50,
    ) -> List[Dict[str, Any]]:
        """Paginates through an endpoint collection safely."""
        all_items: List[Dict[str, Any]] = []
        current_params = dict(params or {})
        current_params.setdefault("limit", page_size)
        cursor: Optional[str] = None
        page = 0

        while page < max_pages:
            if cursor:
                current_params["cursor"] = cursor
            try:
                res = await self.fetch_endpoint(endpoint, params=current_params)
                data = res["data"]
                items = data.get("items", data if isinstance(data, list) else [])
                all_items.extend(items)
                cursor = data.get("next_cursor") if isinstance(data, dict) else None
                if not cursor or not items:
                    break
                page += 1
            except Exception as e:
                logger.warning("Pagination halted at page %d on %s: %s", page, endpoint, e)
                break

        return all_items
