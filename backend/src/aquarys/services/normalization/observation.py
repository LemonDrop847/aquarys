"""Observation entity normalizer."""

from datetime import UTC, datetime
from typing import Any


def normalize_observation(
    raw: dict[str, Any], raw_payload_hash: str | None = None
) -> dict[str, Any]:
    """Normalizes raw citizen / field observation into canonical schema dict.

    Preserves all unmapped / extra fields in metadata_json.
    """
    raw_copy = dict(raw)

    obs_id = str(raw_copy.pop("id", raw_copy.pop("observation_id", "")))
    site_id = str(raw_copy.pop("site_id", ""))

    observed_at_str = raw_copy.pop("observed_at", raw_copy.pop("timestamp", None))
    if observed_at_str:
        try:
            observed_at = datetime.fromisoformat(str(observed_at_str).replace("Z", "+00:00"))
        except Exception:
            observed_at = datetime.now(UTC)
    else:
        observed_at = datetime.now(UTC)

    observer_type = str(raw_copy.pop("observer_type", "citizen"))
    observer_id = raw_copy.pop("observer_id", None)
    if observer_id is not None:
        observer_id = str(observer_id)

    lat = float(raw_copy.pop("latitude", raw_copy.pop("lat", 0.0)))
    lon = float(raw_copy.pop("longitude", raw_copy.pop("lon", raw_copy.pop("lng", 0.0))))

    water_clarity = raw_copy.pop("water_clarity", raw_copy.pop("clarity", None))
    flow_rate_category = raw_copy.pop("flow_rate_category", raw_copy.pop("flow_rate", None))
    odor = raw_copy.pop("odor", raw_copy.pop("odour", None))

    algae = raw_copy.pop("algae_coverage_pct", raw_copy.pop("algae_coverage", None))
    algae_coverage_pct = float(algae) if algae is not None else None

    litter = raw_copy.pop("litter_present", raw_copy.pop("litter", None))
    litter_present = bool(litter) if litter is not None else None

    canopy = raw_copy.pop("canopy_cover_pct", raw_copy.pop("canopy_cover", None))
    canopy_cover_pct = float(canopy) if canopy is not None else None

    image_urls = raw_copy.pop("image_urls", raw_copy.pop("images", []))
    if isinstance(image_urls, str):
        image_urls = [image_urls]
    elif not isinstance(image_urls, list):
        image_urls = []

    notes = raw_copy.pop("notes", raw_copy.pop("comment", None))

    # Provenance
    source = str(raw_copy.pop("source", "OAH"))
    source_id = raw_copy.pop("source_id", obs_id)
    source_endpoint = raw_copy.pop("source_endpoint", f"/observations/{obs_id}")

    retrieved_at_str = raw_copy.pop("retrieved_at", None)
    if retrieved_at_str:
        try:
            retrieved_at = datetime.fromisoformat(str(retrieved_at_str).replace("Z", "+00:00"))
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
        "id": obs_id,
        "site_id": site_id,
        "observed_at": observed_at,
        "observer_type": observer_type,
        "observer_id": observer_id,
        "latitude": lat,
        "longitude": lon,
        "water_clarity": water_clarity,
        "flow_rate_category": flow_rate_category,
        "odor": odor,
        "algae_coverage_pct": algae_coverage_pct,
        "litter_present": litter_present,
        "canopy_cover_pct": canopy_cover_pct,
        "image_urls": image_urls,
        "notes": notes,
        "source": source,
        "source_id": str(source_id) if source_id else None,
        "source_endpoint": source_endpoint,
        "retrieved_at": retrieved_at,
        "raw_payload_hash": raw_payload_hash,
        "processing_version": processing_version,
        "metadata_json": metadata_json,
    }
