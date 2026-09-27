"""Earth Observation / Satellite data normalizer."""

from datetime import datetime, timezone
from typing import Any, Dict


def normalize_eo_measurement(raw: Dict[str, Any], raw_payload_hash: str | None = None) -> Dict[str, Any]:
    """Normalizes raw EO/satellite measurement into canonical schema dict.

    Preserves all unmapped / extra fields in metadata_json.
    """
    raw_copy = dict(raw)

    eo_id = str(raw_copy.pop("id", raw_copy.pop("eo_id", "")))
    site_id = str(raw_copy.pop("site_id", ""))

    observed_at_str = raw_copy.pop("observed_at", raw_copy.pop("acquired_at", raw_copy.pop("timestamp", None)))
    if observed_at_str:
        try:
            observed_at = datetime.fromisoformat(str(observed_at_str).replace("Z", "+00:00"))
        except Exception:
            observed_at = datetime.now(timezone.utc)
    else:
        observed_at = datetime.now(timezone.utc)

    satellite_source = str(raw_copy.pop("satellite_source", raw_copy.pop("satellite", "Sentinel-2")))

    # Check direct index columns
    ndvi = raw_copy.pop("ndvi", None)
    ndwi = raw_copy.pop("ndwi", None)
    surface_temp_c = raw_copy.pop("surface_temp_c", raw_copy.pop("surface_temperature", None))

    # Check band_or_index / product representation
    band_or_index = str(raw_copy.pop("band_or_index", raw_copy.pop("index", ""))).upper()
    val = raw_copy.pop("mean_value", raw_copy.pop("value", None))
    val_float = float(val) if val is not None else None

    if band_or_index == "NDVI" and ndvi is None and val_float is not None:
        ndvi = val_float
    elif band_or_index == "NDWI" and ndwi is None and val_float is not None:
        ndwi = val_float
    elif band_or_index in ("LST", "LST_C", "SURFACE_TEMP", "TEMPERATURE") and surface_temp_c is None and val_float is not None:
        surface_temp_c = val_float
    elif band_or_index and val_float is not None:
        # Preserve specific index value under metadata
        raw_copy[f"index_{band_or_index.lower()}_value"] = val_float

    cloud = raw_copy.pop("cloud_cover_pct", raw_copy.pop("cloud_cover_percentage", raw_copy.pop("cloud_cover", None)))
    cloud_cover_pct = float(cloud) if cloud is not None else None

    res = raw_copy.pop("resolution_m", raw_copy.pop("resolution", 10.0))
    resolution_m = float(res) if res is not None else 10.0

    # Provenance
    source = str(raw_copy.pop("source", "OAH-EO"))
    source_id = raw_copy.pop("source_id", eo_id)
    source_endpoint = raw_copy.pop("source_endpoint", f"/eo/measurements/{eo_id}")

    retrieved_at_str = raw_copy.pop("retrieved_at", None)
    if retrieved_at_str:
        try:
            retrieved_at = datetime.fromisoformat(str(retrieved_at_str).replace("Z", "+00:00"))
        except Exception:
            retrieved_at = datetime.now(timezone.utc)
    else:
        retrieved_at = datetime.now(timezone.utc)

    processing_version = str(raw_copy.pop("processing_version", "1.0.0"))

    # Metadata preservation
    existing_meta = raw_copy.pop("metadata", {})
    if not isinstance(existing_meta, dict):
        existing_meta = {"raw_meta": existing_meta}
    metadata_json = {**existing_meta, **raw_copy}

    return {
        "id": eo_id,
        "site_id": site_id,
        "observed_at": observed_at,
        "satellite_source": satellite_source,
        "ndvi": float(ndvi) if ndvi is not None else None,
        "ndwi": float(ndwi) if ndwi is not None else None,
        "surface_temp_c": float(surface_temp_c) if surface_temp_c is not None else None,
        "cloud_cover_pct": cloud_cover_pct,
        "resolution_m": resolution_m,
        "source": source,
        "source_id": str(source_id) if source_id else None,
        "source_endpoint": source_endpoint,
        "retrieved_at": retrieved_at,
        "raw_payload_hash": raw_payload_hash,
        "processing_version": processing_version,
        "metadata_json": metadata_json,
    }
