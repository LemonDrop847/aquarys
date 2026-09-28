"""Pydantic schemas for the Evidence Graph."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EvidenceNodeSchema(BaseModel):
    id: str
    node_type: str = Field(
        description="CLAIM, OBSERVATION, MEASUREMENT, EO_SIGNAL, SITE, HYPOTHESIS, INTERVENTION"
    )
    label: str
    description: str | None = None
    confidence: float = 1.0
    source_reference: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class EvidenceEdgeSchema(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    edge_type: str = Field(
        description="supports, contradicts, derived_from, correlates, located_at"
    )
    weight: float = 1.0
    reason: str | None = None
    created_at: datetime


class EvidenceGraphResponse(BaseModel):
    site_id: str
    node_count: int
    edge_count: int
    contradiction_count: int = 0
    support_count: int = 0
    nodes: list[EvidenceNodeSchema] = Field(default_factory=list)
    edges: list[EvidenceEdgeSchema] = Field(default_factory=list)
