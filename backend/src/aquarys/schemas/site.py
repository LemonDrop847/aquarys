"""Site Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SiteBase(BaseModel):
    code: str
    name: str
    city: str
    country: str = "Portugal"
    stream_name: str | None = None
    latitude: float
    longitude: float
    altitude_m: float | None = None
    catchment_area_km2: float | None = None
    is_hero: bool = False
    description: str | None = None
    source: str = "OAH"
    source_id: str | None = None
    source_endpoint: str | None = None
    retrieved_at: datetime | None = None
    raw_payload_hash: str | None = None
    processing_version: str = "1.0.0"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class SiteResponse(SiteBase):
    model_config = ConfigDict(from_attributes=True)

    id: str


class SiteListResponse(BaseModel):
    items: list[SiteResponse]
    total: int


class TimelineEvent(BaseModel):
    id: str
    site_id: str
    event_type: str  # "observation", "measurement", "eo_measurement"
    observed_at: datetime
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)


class SiteTimelineResponse(BaseModel):
    site_id: str
    total: int
    events: list[TimelineEvent]
