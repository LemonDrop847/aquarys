"""Pydantic schemas for Knowledge Gaps and Volunteer Mission Optimization."""

from datetime import datetime

from pydantic import BaseModel, Field


class KnowledgeGapItem(BaseModel):
    dimension: str
    gap_type: str = "MISSING_DIMENSION"
    severity: float = Field(default=0.5, ge=0.0, le=1.0)
    status: str = "missing"
    reason: str
    recommended_action: str
    suggested_task_type: str
    priority: str = "HIGH"
    suggested_offset_km: float = 0.0


class KnowledgeGapsResponse(BaseModel):
    site_id: str
    gap_count: int
    gaps: list[KnowledgeGapItem] = Field(default_factory=list)


class InformationGainResponse(BaseModel):
    site_id: str
    dimension: str
    dimension_status: str
    prior_uncertainty: float
    expected_posterior_uncertainty: float
    expected_information_gain: float
    prior_shannon_entropy: float
    observation_resolving_power: float
    reasoning: str


class MissionTaskSchema(BaseModel):
    id: str
    mission_id: str
    volunteer_index: int
    volunteer_name: str
    target_location_name: str
    latitude: float
    longitude: float
    target_observation_type: str
    priority: str = "HIGH"
    estimated_duration_min: int = 15
    expected_gain: float = 0.25
    instructions: str


class MissionOptimizeRequest(BaseModel):
    site_id: str
    volunteer_count: int = Field(default=5, ge=1, le=50)
    available_time_minutes: int = Field(default=60, ge=15, le=480)
    focus_dimensions: list[str] | None = None
    persist: bool = True


class MissionResponse(BaseModel):
    id: str
    title: str
    objective: str
    target_site_id: str
    volunteer_count: int
    available_time_minutes: int
    expected_information_gain: float
    coverage_improvement_pct: float
    gaps_addressed: list[str] = Field(default_factory=list)
    tasks: list[MissionTaskSchema] = Field(default_factory=list)
    created_at: datetime | None = None
