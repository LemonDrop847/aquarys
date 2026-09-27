"""Snapshot ingestion service for offline and reproducible operation."""

import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timezone

from aquarys.core.logging import logger
from aquarys.services.ingestion.client import OAHClient

SNAPSHOTS_DIR = Path(__file__).resolve().parents[4] / "data" / "snapshots"
RAW_DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "raw"


class SnapshotIngestionService:
    """Loads curated offline data snapshots and produces provenance-tracked payloads."""

    def __init__(self, snapshots_dir: Path | None = None, raw_dir: Path | None = None) -> None:
        self.snapshots_dir = snapshots_dir or SNAPSHOTS_DIR
        self.raw_dir = raw_dir or RAW_DATA_DIR
        self.client = OAHClient(raw_storage_dir=self.raw_dir)

    def load_snapshot(self, entity_name: str) -> List[Dict[str, Any]]:
        """Loads a snapshot JSON file by entity name."""
        file_path = self.snapshots_dir / f"{entity_name}.json"
        if not file_path.exists():
            logger.warning("Snapshot file not found: %s", file_path)
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]

    def ingest_snapshot(self, entity_name: str) -> Dict[str, Any]:
        """Loads snapshot, computes hash, persists raw payload, returns ingestion bundle."""
        items = self.load_snapshot(entity_name)
        endpoint = f"/{entity_name}"
        payload_hash = self.client.compute_hash(items)
        raw_path = self.client._persist_raw_payload(endpoint, items, payload_hash)

        return {
            "entity": entity_name,
            "endpoint": endpoint,
            "items": items,
            "count": len(items),
            "payload_hash": payload_hash,
            "raw_storage_path": str(raw_path),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        }

    def ingest_all_snapshots(self) -> Dict[str, Any]:
        """Ingests all available snapshots in data/snapshots/."""
        entities = ["sites", "observations", "measurements", "eo_measurements"]
        results = {}
        for entity in entities:
            res = self.ingest_snapshot(entity)
            results[entity] = res
            logger.info("Ingested snapshot '%s' with %d records (hash: %s)", entity, res["count"], res["payload_hash"][:8])
        return results
