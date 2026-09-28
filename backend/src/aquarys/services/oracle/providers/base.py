"""Base protocol and types for LLM reasoning providers."""

from typing import Any, Protocol, runtime_checkable
from pydantic import BaseModel, Field


class HypothesisResult(BaseModel):
    id: str
    statement: str
    plausibility_score: float = Field(default=0.7, ge=0.0, le=1.0)
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    counter_evidence: str | None = None
    skeptic_challenge: str | None = None
    remaining_uncertainty: str | None = None


class InvestigationSynthesis(BaseModel):
    finding: str
    facts: list[str] = Field(default_factory=list)
    hypotheses: list[HypothesisResult] = Field(default_factory=list)
    counter_evidence: list[str] = Field(default_factory=list)
    data_gaps: list[dict[str, Any]] = Field(default_factory=list)
    next_observations: list[dict[str, Any]] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class ChallengeResult(BaseModel):
    hypothesis_id: str
    original_plausibility: float
    adjusted_plausibility: float
    skeptic_critique: str
    identified_counter_evidence: list[str]
    epistemic_weaknesses: list[str]
    suggested_verification_test: str


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol defining swappable LLM providers for the Oracle."""

    async def synthesize_investigation(
        self,
        site_context: dict[str, Any],
        evidence_graph: dict[str, Any],
        twin_context: list[dict[str, Any]],
        question: str,
    ) -> InvestigationSynthesis:
        """Synthesize a grounded investigation report from multi-source evidence."""
        ...

    async def challenge_hypothesis(
        self,
        hypothesis_statement: str,
        supporting_evidence: list[dict[str, Any]],
        site_context: dict[str, Any],
    ) -> ChallengeResult:
        """Perform adversarial critique against a hypothesis."""
        ...
