"""Observation Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ObservationBase(BaseModel):
    site_id: str
    observed_at: datetime
    observer_type: str = "citizen"
    observer_id: str | None = None
    latitude: float
    longitude: float
    water_clarity: str | None = None
    flow_rate_category: str | None = None
    odor: str | None = None
    algae_coverage_pct: float | None = None
    litter_present: bool | None = None
    canopy_cover_pct: float | None = None
    image_urls: list[str | dict[str, Any]] = Field(default_factory=list)
    notes: str | None = None
    source: str = "OAH"
    source_id: str | None = None
    source_endpoint: str | None = None
    retrieved_at: datetime | None = None
    raw_payload_hash: str | None = None
    processing_version: str = "1.0.0"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ObservationResponse(ObservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str


class ObservationListResponse(BaseModel):
    items: list[ObservationResponse]
    total: int
