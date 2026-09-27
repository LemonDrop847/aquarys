"""Measurement Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MeasurementBase(BaseModel):
    site_id: str
    observed_at: datetime
    parameter: str
    value: float
    unit: str
    quality_flag: str | None = "valid"
    source: str = "OAH"
    source_id: str | None = None
    source_endpoint: str | None = None
    retrieved_at: datetime | None = None
    raw_payload_hash: str | None = None
    processing_version: str = "1.0.0"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class MeasurementResponse(MeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: str


class MeasurementListResponse(BaseModel):
    items: list[MeasurementResponse]
    total: int
