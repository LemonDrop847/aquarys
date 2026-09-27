"""Measurement entity normalizer."""

from datetime import datetime, timezone
from typing import Any, Dict


def normalize_measurement(raw: Dict[str, Any], raw_payload_hash: str | None = None) -> Dict[str, Any]:
    """Normalizes raw physical / chemical measurement into canonical schema dict.

    Preserves all unmapped / extra fields in metadata_json.
    """
    raw_copy = dict(raw)

    mea_id = str(raw_copy.pop("id", raw_copy.pop("measurement_id", "")))
    site_id = str(raw_copy.pop("site_id", ""))

    observed_at_str = raw_copy.pop("observed_at", raw_copy.pop("measured_at", raw_copy.pop("timestamp", None)))
    if observed_at_str:
        try:
            observed_at = datetime.fromisoformat(str(observed_at_str).replace("Z", "+00:00"))
        except Exception:
            observed_at = datetime.now(timezone.utc)
    else:
        observed_at = datetime.now(timezone.utc)

    parameter = str(raw_copy.pop("parameter", raw_copy.pop("param", "unknown")))
    val = raw_copy.pop("value", raw_copy.pop("val", 0.0))
    value = float(val) if val is not None else 0.0

    unit = str(raw_copy.pop("unit", ""))
    quality_flag = str(raw_copy.pop("quality_flag", raw_copy.pop("flag", "good")))

    device_id = raw_copy.pop("device_id", raw_copy.pop("sensor_id", None))
    if device_id is not None:
        device_id = str(device_id)

    # Provenance
    source = str(raw_copy.pop("source", "OAH"))
    source_id = raw_copy.pop("source_id", mea_id)
    source_endpoint = raw_copy.pop("source_endpoint", f"/measurements/{mea_id}")

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
        "id": mea_id,
        "site_id": site_id,
        "observed_at": observed_at,
        "parameter": parameter,
        "value": value,
        "unit": unit,
        "quality_flag": quality_flag,
        "device_id": device_id,
        "source": source,
        "source_id": str(source_id) if source_id else None,
        "source_endpoint": source_endpoint,
        "retrieved_at": retrieved_at,
        "raw_payload_hash": raw_payload_hash,
        "processing_version": processing_version,
        "metadata_json": metadata_json,
    }
