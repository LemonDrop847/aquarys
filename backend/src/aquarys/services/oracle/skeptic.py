"""Adversarial Skeptic Engine challenging causal hypotheses against real telemetry."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.schemas.oracle import ChallengeRequest, ChallengeResponse
from aquarys.services.oracle.providers import get_llm_provider
from aquarys.services.oracle.tools import tool_get_evidence, tool_get_site_profile


def _now() -> str:
    return datetime.now(UTC).isoformat()


async def challenge_hypothesis_epistemic(
    db: AsyncSession,
    request: ChallengeRequest,
) -> ChallengeResponse:
    """Performs adversarial critique against a specific hypothesis."""
    activity_events: list[dict[str, Any]] = []

    activity_events.append({
        "timestamp": _now(),
        "tool": "tool_get_site_profile",
        "description": f"Retrieving site profile for context verification on {request.site_id}",
    })
    site_profile = await tool_get_site_profile(db, request.site_id) or {"site_id": request.site_id}

    activity_events.append({
        "timestamp": _now(),
        "tool": "tool_get_evidence",
        "description": "Extracting counter-evidence and anomaly edges from relational graph",
    })
    evidence = await tool_get_evidence(db, request.site_id)
    contradictions = evidence.get("contradictions", [])

    activity_events.append({
        "timestamp": _now(),
        "tool": "llm_provider.challenge_hypothesis",
        "description": "Generating adversarial critique and proposing verification tests",
    })
    provider = get_llm_provider(request.provider)
    res = await provider.challenge_hypothesis(
        hypothesis_statement=request.hypothesis_statement,
        supporting_evidence=contradictions,
        site_context=site_profile,
    )

    return ChallengeResponse(
        hypothesis_id=request.hypothesis_id or res.hypothesis_id,
        original_plausibility=res.original_plausibility,
        adjusted_plausibility=res.adjusted_plausibility,
        skeptic_critique=res.skeptic_critique,
        identified_counter_evidence=res.identified_counter_evidence,
        epistemic_weaknesses=res.epistemic_weaknesses,
        suggested_verification_test=res.suggested_verification_test,
        activity_events=activity_events,
        provider_used=request.provider or "demo",
    )
