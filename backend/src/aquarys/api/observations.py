"""Observation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.models import Observation
from aquarys.schemas.observation import ObservationListResponse, ObservationResponse

router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("", response_model=ObservationListResponse)
async def list_observations(
    site_id: str | None = Query(None, description="Filter by site ID"),
    observer_type: str | None = Query(
        None, description="Filter by observer type (citizen, researcher, sensor)"
    ),
    water_clarity: str | None = Query(None, description="Filter by water clarity"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Observation)
    if site_id:
        query = query.where(Observation.site_id == site_id)
    if observer_type:
        query = query.where(Observation.observer_type == observer_type)
    if water_clarity:
        query = query.where(Observation.water_clarity == water_clarity)

    query = query.order_by(desc(Observation.observed_at)).limit(limit).offset(offset)
    result = await db.execute(query)
    observations = result.scalars().all()

    count_query = select(Observation)
    if site_id:
        count_query = count_query.where(Observation.site_id == site_id)
    if observer_type:
        count_query = count_query.where(Observation.observer_type == observer_type)
    if water_clarity:
        count_query = count_query.where(Observation.water_clarity == water_clarity)
    count_res = await db.execute(count_query)
    total = len(count_res.scalars().all())

    return ObservationListResponse(
        items=[ObservationResponse.model_validate(obs) for obs in observations],
        total=total,
    )


@router.get("/{observation_id}", response_model=ObservationResponse)
async def get_observation(observation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Observation).where(Observation.id == observation_id))
    obs = result.scalar_one_or_none()
    if not obs:
        raise HTTPException(
            status_code=404, detail=f"Observation with id '{observation_id}' not found"
        )
    return ObservationResponse.model_validate(obs)
