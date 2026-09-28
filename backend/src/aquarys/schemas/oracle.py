"""Schemas for Oracle reasoning, investigations, and hypothesis challenges."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    site_id: str
    question: str = Field(
        default="What is the current ecological status of this stream, and what is driving observed degradation?",
        description="Scientific or investigative question for the Oracle.",
    )
    provider: str | None = Field(
        default=None,
        description="Optional LLM provider override ('demo', 'gemini', 'ollama').",
    )


class HypothesisSchema(BaseModel):
    id: str
    statement: str
    plausibility_score: float = Field(default=0.7, ge=0.0, le=1.0)
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    counter_evidence: str | None = None
    skeptic_challenge: str | None = None
    remaining_uncertainty: str | None = None


class InvestigationResponse(BaseModel):
    id: str
    site_id: str
    question: str
    finding: str
    facts: list[str] = Field(default_factory=list)
    hypotheses: list[HypothesisSchema] = Field(default_factory=list)
    counter_evidence: list[str] = Field(default_factory=list)
    data_gaps: list[dict[str, Any]] = Field(default_factory=list)
    next_observations: list[dict[str, Any]] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    activity_events: list[dict[str, Any]] = Field(default_factory=list)
    provider_used: str
    created_at: datetime


class ChallengeRequest(BaseModel):
    hypothesis_id: str | None = None
    hypothesis_statement: str
    site_id: str
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    provider: str | None = None


class ChallengeResponse(BaseModel):
    hypothesis_id: str
    original_plausibility: float
    adjusted_plausibility: float
    skeptic_critique: str
    identified_counter_evidence: list[str] = Field(default_factory=list)
    epistemic_weaknesses: list[str] = Field(default_factory=list)
    suggested_verification_test: str
    activity_events: list[dict[str, Any]] = Field(default_factory=list)
    provider_used: str
