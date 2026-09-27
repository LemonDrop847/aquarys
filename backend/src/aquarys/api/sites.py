"""Site API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.models import EOMeasurement, Measurement, Observation, Site
from aquarys.schemas.site import SiteListResponse, SiteResponse, SiteTimelineResponse, TimelineEvent

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("", response_model=SiteListResponse)
async def list_sites(
    city: str | None = Query(None, description="Filter by city name"),
    country: str | None = Query(None, description="Filter by country"),
    is_hero: bool | None = Query(None, description="Filter by hero status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Site)
    if city:
        query = query.where(Site.city.ilike(f"%{city}%"))
    if country:
        query = query.where(Site.country.ilike(f"%{country}%"))
    if is_hero is not None:
        query = query.where(Site.is_hero == is_hero)

    query = query.order_by(Site.code.asc()).limit(limit).offset(offset)
    result = await db.execute(query)
    sites = result.scalars().all()

    # Total count query
    count_query = select(Site)
    if city:
        count_query = count_query.where(Site.city.ilike(f"%{city}%"))
    if country:
        count_query = count_query.where(Site.country.ilike(f"%{country}%"))
    if is_hero is not None:
        count_query = count_query.where(Site.is_hero == is_hero)
    count_res = await db.execute(count_query)
    total = len(count_res.scalars().all())

    return SiteListResponse(items=[SiteResponse.model_validate(s) for s in sites], total=total)


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(site_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail=f"Site with id '{site_id}' not found")
    return SiteResponse.model_validate(site)


@router.get("/{site_id}/timeline", response_model=SiteTimelineResponse)
async def get_site_timeline(
    site_id: str,
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    site_res = await db.execute(select(Site).where(Site.id == site_id))
    site = site_res.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail=f"Site with id '{site_id}' not found")

    events = []

    # Fetch observations
    obs_res = await db.execute(
        select(Observation)
        .where(Observation.site_id == site_id)
        .order_by(desc(Observation.observed_at))
        .limit(limit)
    )
    for obs in obs_res.scalars().all():
        summary = f"Citizen observation ({obs.observer_type}): clarity={obs.water_clarity or 'unknown'}, flow={obs.flow_rate_category or 'unknown'}"
        events.append(
            TimelineEvent(
                id=obs.id,
                site_id=site_id,
                event_type="observation",
                observed_at=obs.observed_at,
                summary=summary,
                data={
                    "water_clarity": obs.water_clarity,
                    "flow_rate_category": obs.flow_rate_category,
                    "odor": obs.odor,
                    "algae_coverage_pct": obs.algae_coverage_pct,
                    "image_count": len(obs.image_urls or []),
                },
            )
        )

    # Fetch measurements
    meas_res = await db.execute(
        select(Measurement)
        .where(Measurement.site_id == site_id)
        .order_by(desc(Measurement.observed_at))
        .limit(limit)
    )
    for m in meas_res.scalars().all():
        summary = f"Physical measurement: {m.parameter} = {m.value} {m.unit}"
        events.append(
            TimelineEvent(
                id=m.id,
                site_id=site_id,
                event_type="measurement",
                observed_at=m.observed_at,
                summary=summary,
                data={
                    "parameter": m.parameter,
                    "value": m.value,
                    "unit": m.unit,
                    "quality_flag": m.quality_flag,
                },
            )
        )

    # Fetch EO measurements
    eo_res = await db.execute(
        select(EOMeasurement)
        .where(EOMeasurement.site_id == site_id)
        .order_by(desc(EOMeasurement.observed_at))
        .limit(limit)
    )
    for eo in eo_res.scalars().all():
        summary = f"Earth Observation ({eo.satellite_source}): NDVI={eo.ndvi}, NDWI={eo.ndwi}"
        events.append(
            TimelineEvent(
                id=eo.id,
                site_id=site_id,
                event_type="eo_measurement",
                observed_at=eo.observed_at,
                summary=summary,
                data={
                    "satellite_source": eo.satellite_source,
                    "ndvi": eo.ndvi,
                    "ndwi": eo.ndwi,
                    "cloud_cover_pct": eo.cloud_cover_pct,
                },
            )
        )

    # Sort all events chronologically descending
    events.sort(key=lambda x: x.observed_at, reverse=True)
    return SiteTimelineResponse(site_id=site_id, total=len(events), events=events[:limit])
