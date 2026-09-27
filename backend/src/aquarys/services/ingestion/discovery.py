"""OAH API Discovery service."""

import json
from pathlib import Path
from typing import Any

import httpx

from aquarys.core.config import settings
from aquarys.core.logging import logger

MANIFEST_PATH = Path(__file__).parents[3] / "data" / "api-manifest.json"


async def discover_oah_api(
    base_url: str | None = None, api_key: str | None = None
) -> dict[str, Any]:
    """Inspects OAH endpoints or reads existing manifest."""
    url = base_url or settings.OAH_BASE_URL
    key = api_key or settings.OAH_API_KEY
    headers = {"Authorization": f"Bearer {key}"} if key else {}

    manifest: dict[str, Any] = {
        "service": "OneAquaHealth",
        "base_url": url,
        "endpoints": [],
        "status": "unverified",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{url}/openapi.json", headers=headers)
            if resp.status_code == 200:
                spec = resp.json()
                manifest["status"] = "verified"
                manifest["openapi"] = spec
                manifest["title"] = spec.get("info", {}).get("title", "OAH API")
                for path, methods in spec.get("paths", {}).items():
                    for method, details in methods.items():
                        manifest["endpoints"].append(
                            {
                                "path": path,
                                "method": method.upper(),
                                "summary": details.get("summary", ""),
                                "parameters": details.get("parameters", []),
                            }
                        )
            else:
                logger.warning(
                    "OAH discovery returned status %s. Falling back to cached manifest.",
                    resp.status_code,
                )
                if MANIFEST_PATH.exists():
                    with open(MANIFEST_PATH, encoding="utf-8") as f:
                        return json.load(f)
    except Exception as e:
        logger.warning("Failed to connect to OAH API (%s). Using cached manifest.", e)
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, encoding="utf-8") as f:
                return json.load(f)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest
