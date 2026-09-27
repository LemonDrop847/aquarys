"""Earth Observation Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EOMeasurementBase(BaseModel):
    site_id: str
    observed_at: datetime
    satellite_source: str = "Sentinel-2"
    ndwi: float | None = None
    ndvi: float | None = None
    turbidity_proxy: float | None = None
    cloud_cover_pct: float | None = None
    surface_temp_c: float | None = None
    source: str = "OAH"
    source_id: str | None = None
    source_endpoint: str | None = None
    retrieved_at: datetime | None = None
    raw_payload_hash: str | None = None
    processing_version: str = "1.0.0"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class EOMeasurementResponse(EOMeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: str


class EOMeasurementListResponse(BaseModel):
    items: list[EOMeasurementResponse]
    total: int
