"""API router for Oracle investigation and hypothesis challenge endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.models import OracleInvestigation
from aquarys.schemas.oracle import (
    ChallengeRequest,
    ChallengeResponse,
    HypothesisSchema,
    InvestigationRequest,
    InvestigationResponse,
)
from aquarys.services.oracle.investigator import run_investigation
from aquarys.services.oracle.skeptic import challenge_hypothesis_epistemic

router = APIRouter(prefix="/oracle", tags=["Oracle"])


@router.post("/investigate", response_model=InvestigationResponse)
async def investigate_site(
    request: InvestigationRequest,
    db: AsyncSession = Depends(get_db),
) -> InvestigationResponse:
    """Run an evidence-grounded scientific investigation on a stream site."""
    return await run_investigation(db, request)


@router.post("/challenge", response_model=ChallengeResponse)
async def challenge_hypothesis(
    request: ChallengeRequest,
    db: AsyncSession = Depends(get_db),
) -> ChallengeResponse:
    """Run an adversarial skeptic critique on an ecological hypothesis."""
    return await challenge_hypothesis_epistemic(db, request)


@router.get("/investigations/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: str,
    db: AsyncSession = Depends(get_db),
) -> InvestigationResponse:
    """Retrieve a previously executed investigation by ID."""
    stmt = select(OracleInvestigation).where(OracleInvestigation.id == investigation_id)
    res = await db.execute(stmt)
    inv = res.scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found")

    return InvestigationResponse(
        id=inv.id,
        site_id=inv.site_id,
        question=inv.question,
        finding=inv.finding,
        facts=inv.facts or [],
        hypotheses=[HypothesisSchema(**h) for h in (inv.hypotheses or [])],
        counter_evidence=inv.counter_evidence or [],
        data_gaps=inv.data_gaps or [],
        next_observations=inv.next_observations or [],
        caveats=inv.caveats or [],
        evidence_ids=inv.evidence_ids or [],
        activity_events=inv.activity_events or [],
        provider_used=inv.provider_used,
        created_at=inv.created_at,
    )
