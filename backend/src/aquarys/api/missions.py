"""API router for Knowledge Gaps and Mission Optimization endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aquarys.core.database import get_db
from aquarys.models import Mission, Site
from aquarys.schemas.mission import (
    InformationGainResponse,
    KnowledgeGapItem,
    KnowledgeGapsResponse,
    MissionOptimizeRequest,
    MissionResponse,
    MissionTaskSchema,
)
from aquarys.services.missions.gaps import detect_knowledge_gaps
from aquarys.services.missions.information_gain import calculate_dimension_information_gain
from aquarys.services.missions.optimizer import optimize_mission

router = APIRouter(prefix="/missions", tags=["Missions & Knowledge Gaps"])


@router.get("/gaps/{site_id}", response_model=KnowledgeGapsResponse)
async def get_site_knowledge_gaps(
    site_id: str,
    db: AsyncSession = Depends(get_db),
) -> KnowledgeGapsResponse:
    """Retrieve detected epistemic knowledge gaps and data voids for a site."""
    site_stmt = select(Site).where(Site.id == site_id)
    site_res = await db.execute(site_stmt)
    if not site_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Site {site_id} not found")

    gaps_data = await detect_knowledge_gaps(db, site_id)
    return KnowledgeGapsResponse(
        site_id=site_id,
        gap_count=len(gaps_data),
        gaps=[KnowledgeGapItem(**g) for g in gaps_data],
    )


@router.get("/gain/{site_id}/{dimension}", response_model=InformationGainResponse)
async def get_information_gain(
    site_id: str,
    dimension: str,
    db: AsyncSession = Depends(get_db),
) -> InformationGainResponse:
    """Calculate expected information gain and entropy reduction for a target dimension."""
    site_stmt = select(Site).where(Site.id == site_id)
    site_res = await db.execute(site_stmt)
    if not site_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Site {site_id} not found")

    gain_data = await calculate_dimension_information_gain(db, site_id, dimension)
    return InformationGainResponse(**gain_data)


@router.post("/optimize", response_model=MissionResponse)
async def create_optimized_mission(
    request: MissionOptimizeRequest,
    db: AsyncSession = Depends(get_db),
) -> MissionResponse:
    """Run multi-objective optimization to generate a targeted volunteer mission."""
    try:
        mission_dict = await optimize_mission(
            db=db,
            site_id=request.site_id,
            volunteer_count=request.volunteer_count,
            available_time_minutes=request.available_time_minutes,
            focus_dimensions=request.focus_dimensions,
            persist=request.persist,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return MissionResponse(
        id=mission_dict["id"],
        title=mission_dict["title"],
        objective=mission_dict["objective"],
        target_site_id=mission_dict["target_site_id"],
        volunteer_count=mission_dict["volunteer_count"],
        available_time_minutes=mission_dict["available_time_minutes"],
        expected_information_gain=mission_dict["expected_information_gain"],
        coverage_improvement_pct=mission_dict["coverage_improvement_pct"],
        gaps_addressed=mission_dict["gaps_addressed"],
        tasks=[MissionTaskSchema(**t) for t in mission_dict["tasks"]],
    )


@router.get("/{mission_id}", response_model=MissionResponse)
async def get_mission(
    mission_id: str,
    db: AsyncSession = Depends(get_db),
) -> MissionResponse:
    """Retrieve an existing mission and its volunteer task allocations."""
    stmt = select(Mission).options(selectinload(Mission.tasks)).where(Mission.id == mission_id)
    res = await db.execute(stmt)
    mission = res.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} not found")

    return MissionResponse(
        id=mission.id,
        title=mission.title,
        objective=mission.objective,
        target_site_id=mission.target_site_id,
        volunteer_count=mission.volunteer_count,
        available_time_minutes=mission.available_time_minutes,
        expected_information_gain=mission.expected_information_gain,
        coverage_improvement_pct=mission.coverage_improvement_pct,
        gaps_addressed=mission.gaps_addressed or [],
        tasks=[
            MissionTaskSchema(
                id=t.id,
                mission_id=t.mission_id,
                volunteer_index=t.volunteer_index,
                volunteer_name=t.volunteer_name,
                target_location_name=t.target_location_name,
                latitude=t.latitude,
                longitude=t.longitude,
                target_observation_type=t.target_observation_type,
                priority=t.priority,
                estimated_duration_min=t.estimated_duration_min,
                expected_gain=t.expected_gain,
                instructions=t.instructions,
            )
            for t in sorted(mission.tasks, key=lambda x: x.volunteer_index)
        ],
        created_at=mission.created_at,
    )


@router.get("", response_model=list[MissionResponse])
async def list_missions(
    site_id: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[MissionResponse]:
    """List recent missions, optionally filtered by site."""
    stmt = (
        select(Mission)
        .options(selectinload(Mission.tasks))
        .order_by(Mission.created_at.desc())
        .limit(limit)
    )
    if site_id:
        stmt = stmt.where(Mission.target_site_id == site_id)

    res = await db.execute(stmt)
    missions = res.scalars().all()

    return [
        MissionResponse(
            id=m.id,
            title=m.title,
            objective=m.objective,
            target_site_id=m.target_site_id,
            volunteer_count=m.volunteer_count,
            available_time_minutes=m.available_time_minutes,
            expected_information_gain=m.expected_information_gain,
            coverage_improvement_pct=m.coverage_improvement_pct,
            gaps_addressed=m.gaps_addressed or [],
            tasks=[
                MissionTaskSchema(
                    id=t.id,
                    mission_id=t.mission_id,
                    volunteer_index=t.volunteer_index,
                    volunteer_name=t.volunteer_name,
                    target_location_name=t.target_location_name,
                    latitude=t.latitude,
                    longitude=t.longitude,
                    target_observation_type=t.target_observation_type,
                    priority=t.priority,
                    estimated_duration_min=t.estimated_duration_min,
                    expected_gain=t.expected_gain,
                    instructions=t.instructions,
                )
                for t in sorted(m.tasks, key=lambda x: x.volunteer_index)
            ],
            created_at=m.created_at,
        )
        for m in missions
    ]
