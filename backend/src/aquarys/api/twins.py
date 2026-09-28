"""FastAPI router for Stream Twins."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.models import StreamSimilarity
from aquarys.services.twins.search import search_twins

router = APIRouter(tags=["Stream Twins"])


class TwinSearchRequest(BaseModel):
    target_site_id: str
    limit: int = 5
    min_similarity: float = 0.5


class StreamSimilarityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    site_a_id: str
    site_b_id: str
    overall_similarity: float
    vector_similarity: float
    feature_similarity: float
    temporal_alignment: float
    data_coverage: float
    evidence_confidence: float
    match_signals: dict[str, str]
    differentiators: list[str]


@router.post(
    "/twins/search",
    response_model=list[StreamSimilarityResponse],
    summary="Search for ecological twins for a target site",
)
async def search_twins_endpoint(
    payload: TwinSearchRequest,
    db: AsyncSession = Depends(get_db),
) -> list[StreamSimilarityResponse]:
    """Finds the most similar stream sites using vector embeddings and multi-dimensional feature scoring."""
    twins = await search_twins(
        db=db,
        target_site_id=payload.target_site_id,
        limit=payload.limit,
        min_similarity=payload.min_similarity,
    )
    return [StreamSimilarityResponse.model_validate(t) for t in twins]


@router.get(
    "/twins/{site_a}/{site_b}",
    response_model=StreamSimilarityResponse,
    summary="Get detailed similarity comparison between two specific sites",
)
async def get_twin_comparison(
    site_a: str,
    site_b: str,
    db: AsyncSession = Depends(get_db),
) -> StreamSimilarityResponse:
    """Returns a detailed differential comparison between two sites."""
    # First check if we have a precomputed similarity
    sim_id_1 = f"{site_a}_{site_b}"
    sim_id_2 = f"{site_b}_{site_a}"

    result = await db.execute(
        select(StreamSimilarity).where(StreamSimilarity.id.in_([sim_id_1, sim_id_2]))
    )
    sim = result.scalar_one_or_none()

    if sim:
        return StreamSimilarityResponse.model_validate(sim)

    # If not, calculate on the fly by forcing a search that matches site_b
    twins = await search_twins(db, target_site_id=site_a, limit=100, min_similarity=0.0)
    for t in twins:
        if t.site_b_id == site_b:
            return StreamSimilarityResponse.model_validate(t)

    raise HTTPException(
        status_code=404,
        detail="Comparison not possible. Ensure both sites have generated fingerprints/embeddings.",
    )
