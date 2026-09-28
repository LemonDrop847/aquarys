"""Evidence and Trust Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TrustEvaluateRequest(BaseModel):
    """Request payload to evaluate trust for an observation."""

    observation_id: str | None = None
    observation_data: dict[str, Any] | None = None
    persist: bool = True


class EvidenceAssessmentResponse(BaseModel):
    """Standardized response schema for evidence assessment."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    observation_id: str
    evaluated_at: datetime
    completeness: float
    consistency: float
    location_validity: float
    temporal_validity: float
    image_support: float
    cross_observer: float
    independent_support: float
    duplicate_risk: float
    overall_confidence: float
    flags: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)
    reasoning: str = ""
    processing_version: str = "1.0.0"
