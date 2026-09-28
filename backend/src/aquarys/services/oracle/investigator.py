"""Oracle investigation engine executing multi-step evidence-grounded synthesis."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.models import Hypothesis, OracleInvestigation
from aquarys.schemas.oracle import (
    HypothesisSchema,
    InvestigationRequest,
    InvestigationResponse,
)
from aquarys.services.oracle.providers import get_llm_provider
from aquarys.services.oracle.tools import (
    tool_find_similar_sites,
    tool_get_evidence,
    tool_get_observations,
    tool_get_site_profile,
    tool_get_site_timeline,
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


async def run_investigation(
    db: AsyncSession,
    request: InvestigationRequest,
) -> InvestigationResponse:
    """Orchestrates grounded ecological investigation for a stream site."""
    activity_events: list[dict[str, Any]] = []

    # Step 1: Fetch Site Profile
    activity_events.append(
        {
            "timestamp": _now(),
            "tool": "tool_get_site_profile",
            "description": f"Extracting 9-dimensional ecological fingerprint for site {request.site_id}",
        }
    )
    site_profile = await tool_get_site_profile(db, request.site_id)
    if not site_profile:
        site_profile = {"site_id": request.site_id, "water_quality_score": 50.0}

    # Step 2: Fetch Observations & Timeline
    activity_events.append(
        {
            "timestamp": _now(),
            "tool": "tool_get_observations",
            "description": f"Gathering citizen observations and sensor measurements for site {request.site_id}",
        }
    )
    observations = await tool_get_observations(db, request.site_id, limit=10)
    timeline = await tool_get_site_timeline(db, request.site_id)
    site_profile["observations"] = observations
    site_profile["timeline"] = timeline

    # Step 3: Extract Relational Evidence Graph (Supports / Contradictions)
    activity_events.append(
        {
            "timestamp": _now(),
            "tool": "tool_get_evidence",
            "description": "Constructing relational knowledge graph and detecting cross-modal contradictions",
        }
    )
    evidence_graph = await tool_get_evidence(db, request.site_id)

    # Step 4: Query Ecological Twins for Comparative Context
    activity_events.append(
        {
            "timestamp": _now(),
            "tool": "tool_find_similar_sites",
            "description": "Scanning vector space for comparative ecological twin catchments",
        }
    )
    twins = await tool_find_similar_sites(db, request.site_id, limit=3)

    # Step 5: Provider Reasoning & Epistemic Synthesis
    activity_events.append(
        {
            "timestamp": _now(),
            "tool": "llm_provider.synthesize_investigation",
            "description": f"Synthesizing findings and hypotheses via {request.provider or 'configured'} provider",
        }
    )
    provider = get_llm_provider(request.provider)
    synthesis = await provider.synthesize_investigation(
        site_context=site_profile,
        evidence_graph=evidence_graph,
        twin_context=twins,
        question=request.question,
    )

    investigation_id = f"inv_{uuid.uuid4().hex[:12]}"
    created_at = datetime.now(UTC)

    # Step 6: Persist in Database
    hyp_dicts = [h.model_dump() for h in synthesis.hypotheses]
    inv_model = OracleInvestigation(
        id=investigation_id,
        site_id=request.site_id,
        question=request.question,
        finding=synthesis.finding,
        facts=synthesis.facts,
        hypotheses=hyp_dicts,
        counter_evidence=synthesis.counter_evidence,
        data_gaps=synthesis.data_gaps,
        next_observations=synthesis.next_observations,
        caveats=synthesis.caveats,
        evidence_ids=synthesis.evidence_ids,
        activity_events=activity_events,
        provider_used=request.provider or "demo",
        created_at=created_at,
    )
    db.add(inv_model)

    for h in synthesis.hypotheses:
        hyp_model = Hypothesis(
            id=h.id,
            investigation_id=investigation_id,
            statement=h.statement,
            plausibility_score=h.plausibility_score,
            supporting_evidence_ids=h.supporting_evidence_ids,
            counter_evidence=h.counter_evidence,
            skeptic_challenge=h.skeptic_challenge,
            remaining_uncertainty=h.remaining_uncertainty,
        )
        db.add(hyp_model)

    await db.commit()

    return InvestigationResponse(
        id=investigation_id,
        site_id=request.site_id,
        question=request.question,
        finding=synthesis.finding,
        facts=synthesis.facts,
        hypotheses=[HypothesisSchema(**h.model_dump()) for h in synthesis.hypotheses],
        counter_evidence=synthesis.counter_evidence,
        data_gaps=synthesis.data_gaps,
        next_observations=synthesis.next_observations,
        caveats=synthesis.caveats,
        evidence_ids=synthesis.evidence_ids,
        activity_events=activity_events,
        provider_used=request.provider or "demo",
        created_at=created_at,
    )
