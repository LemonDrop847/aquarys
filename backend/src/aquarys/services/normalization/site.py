"""Site entity normalizer."""

from datetime import UTC, datetime
from typing import Any


def normalize_site(raw: dict[str, Any], raw_payload_hash: str | None = None) -> dict[str, Any]:
    """Normalizes raw site data into canonical schema dict.

    Preserves all unmapped / extra fields in metadata_json.
    """
    raw_copy = dict(raw)

    site_id = str(raw_copy.pop("id", raw_copy.pop("site_id", "")))
    code = str(raw_copy.pop("code", site_id.split("-")[-1] if "-" in site_id else site_id))
    name = str(raw_copy.pop("name", f"Site {code}"))
    city = str(raw_copy.pop("city", "Unknown"))
    country = str(raw_copy.pop("country", "Portugal"))
    stream_name = raw_copy.pop("stream_name", None)

    # Coords
    lat = float(raw_copy.pop("latitude", raw_copy.pop("lat", 0.0)))
    lon = float(raw_copy.pop("longitude", raw_copy.pop("lon", raw_copy.pop("lng", 0.0))))

    alt = raw_copy.pop("altitude_m", raw_copy.pop("altitude", None))
    altitude_m = float(alt) if alt is not None else None

    area = raw_copy.pop("catchment_area_km2", raw_copy.pop("catchment_area", None))
    catchment_area_km2 = float(area) if area is not None else None

    is_hero = bool(raw_copy.pop("is_hero", False))
    description = raw_copy.pop("description", None)

    # Provenance
    source = str(raw_copy.pop("source", "OAH"))
    source_id = raw_copy.pop("source_id", site_id)
    source_endpoint = raw_copy.pop("source_endpoint", f"/sites/{site_id}")

    retrieved_at_str = raw_copy.pop("retrieved_at", None)
    if retrieved_at_str:
        try:
            retrieved_at = datetime.fromisoformat(retrieved_at_str.replace("Z", "+00:00"))
        except Exception:
            retrieved_at = datetime.now(UTC)
    else:
        retrieved_at = datetime.now(UTC)

    processing_version = str(raw_copy.pop("processing_version", "1.0.0"))

    # Metadata preservation
    existing_meta = raw_copy.pop("metadata", {})
    if not isinstance(existing_meta, dict):
        existing_meta = {"raw_meta": existing_meta}
    metadata_json = {**existing_meta, **raw_copy}

    return {
        "id": site_id,
        "code": code,
        "name": name,
        "city": city,
        "country": country,
        "stream_name": stream_name,
        "latitude": lat,
        "longitude": lon,
        "altitude_m": altitude_m,
        "catchment_area_km2": catchment_area_km2,
        "is_hero": is_hero,
        "description": description,
        "source": source,
        "source_id": str(source_id) if source_id else None,
        "source_endpoint": source_endpoint,
        "retrieved_at": retrieved_at,
        "raw_payload_hash": raw_payload_hash,
        "processing_version": processing_version,
        "metadata_json": metadata_json,
    }
