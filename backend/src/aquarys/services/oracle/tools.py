"""Deterministic Oracle evidence tools querying DB, fingerprints, and twins."""

from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aquarys.models import (
    EOMeasurement,
    EvidenceAssessment,
    Measurement,
    Observation,
    Site,
    StreamProfile,
)
from aquarys.services.graph.builder import build_evidence_graph_for_site
from aquarys.services.twins.scoring import calculate_twin_similarity
from aquarys.services.twins.search import search_twins


async def tool_find_sites(
    db: AsyncSession,
    query: str | None = None,
    city: str | None = None,
    country: str | None = None,
) -> list[dict[str, Any]]:
    """Find stream monitoring sites matching query filters."""
    stmt = select(Site)
    if city:
        stmt = stmt.where(Site.city.ilike(f"%{city}%"))
    if country:
        stmt = stmt.where(Site.country.ilike(f"%{country}%"))
    if query:
        stmt = stmt.where(
            (Site.name.ilike(f"%{query}%"))
            | (Site.code.ilike(f"%{query}%"))
            | (Site.id.ilike(f"%{query}%"))
        )
    res = await db.execute(stmt)
    sites = res.scalars().all()
    return [
        {
            "id": s.id,
            "code": s.code,
            "name": s.name,
            "city": s.city,
            "country": s.country,
            "stream_name": s.stream_name,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "is_hero": s.is_hero,
        }
        for s in sites
    ]


async def tool_get_site_profile(db: AsyncSession, site_id: str) -> dict[str, Any] | None:
    """Retrieve ecological fingerprint profile for a site."""
    stmt = (
        select(StreamProfile)
        .where(StreamProfile.site_id == site_id)
        .options(selectinload(StreamProfile.site))
    )
    res = await db.execute(stmt)
    p = res.scalar_one_or_none()
    if not p:
        return None
    return {
        "site_id": p.site_id,
        "site_name": p.site.name if p.site else None,
        "water_quality_score": p.water_quality_score,
        "habitat_score": p.habitat_score,
        "vegetation_score": p.vegetation_score,
        "hydromorphology_score": p.hydromorphology_score,
        "biotics_score": p.biotics_score,
        "nutrients_score": p.nutrients_score,
        "eo_context_score": p.eo_context_score,
        "citizen_evidence_score": p.citizen_evidence_score,
        "climate_context_score": p.climate_context_score,
        "dimension_status": p.dimension_status,
        "data_coverage_pct": p.data_coverage_pct,
        "evidence_confidence_pct": p.evidence_confidence_pct,
    }


async def tool_get_observations(
    db: AsyncSession,
    site_id: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Get recent observations for a site with evidence assessment."""
    stmt = (
        select(Observation)
        .where(Observation.site_id == site_id)
        .options(selectinload(Observation.assessment))
        .order_by(desc(Observation.observed_at))
        .limit(limit)
    )
    res = await db.execute(stmt)
    observations = res.scalars().all()
    return [
        {
            "id": o.id,
            "observed_at": o.observed_at.isoformat() if o.observed_at else None,
            "observer_type": o.observer_type,
            "water_clarity": o.water_clarity,
            "flow_rate_category": o.flow_rate_category,
            "odor": o.odor,
            "algae_coverage_pct": o.algae_coverage_pct,
            "canopy_cover_pct": o.canopy_cover_pct,
            "litter_present": o.litter_present,
            "image_count": len(o.image_urls or []),
            "confidence": o.assessment.overall_confidence if o.assessment else 0.8,
            "flags": o.assessment.flags if o.assessment else [],
        }
        for o in observations
    ]


async def tool_get_site_timeline(db: AsyncSession, site_id: str) -> dict[str, Any]:
    """Retrieve chronological timeline of observations, measurements, and EO data."""
    obs_res = await db.execute(
        select(Observation)
        .where(Observation.site_id == site_id)
        .order_by(desc(Observation.observed_at))
        .limit(20)
    )
    meas_res = await db.execute(
        select(Measurement)
        .where(Measurement.site_id == site_id)
        .order_by(desc(Measurement.observed_at))
        .limit(30)
    )
    eo_res = await db.execute(
        select(EOMeasurement)
        .where(EOMeasurement.site_id == site_id)
        .order_by(desc(EOMeasurement.observed_at))
        .limit(10)
    )

    events = []
    for o in obs_res.scalars().all():
        events.append(
            {
                "timestamp": o.observed_at.isoformat() if o.observed_at else None,
                "type": "observation",
                "id": o.id,
                "summary": f"Citizen observation: clarity={o.water_clarity}, odor={o.odor}",
            }
        )
    for m in meas_res.scalars().all():
        events.append(
            {
                "timestamp": m.observed_at.isoformat() if m.observed_at else None,
                "type": "measurement",
                "id": m.id,
                "summary": f"{m.parameter}: {m.value} {m.unit}",
            }
        )
    for eo in eo_res.scalars().all():
        events.append(
            {
                "timestamp": eo.observed_at.isoformat() if eo.observed_at else None,
                "type": "eo_signal",
                "id": eo.id,
                "summary": f"Sentinel-2 NDVI={eo.ndvi}, NDWI={eo.ndwi}",
            }
        )

    # Sort chronological descending
    events.sort(key=lambda x: x["timestamp"] or "", reverse=True)
    return {"site_id": site_id, "total_events": len(events), "timeline": events}


async def tool_get_observation_quality(
    db: AsyncSession,
    observation_id: str,
) -> dict[str, Any] | None:
    """Get the full Evidence Passport assessment for an observation."""
    stmt = select(EvidenceAssessment).where(EvidenceAssessment.observation_id == observation_id)
    res = await db.execute(stmt)
    ass = res.scalar_one_or_none()
    if not ass:
        return None
    return {
        "assessment_id": ass.id,
        "observation_id": ass.observation_id,
        "overall_confidence": ass.overall_confidence,
        "completeness": ass.completeness,
        "consistency": ass.consistency,
        "location_validity": ass.location_validity,
        "temporal_validity": ass.temporal_validity,
        "image_support": ass.image_support,
        "cross_observer": ass.cross_observer,
        "independent_support": ass.independent_support,
        "duplicate_risk": ass.duplicate_risk,
        "flags": ass.flags,
        "positive_signals": ass.positive_signals,
        "negative_signals": ass.negative_signals,
        "reasoning": ass.reasoning,
    }


async def tool_find_similar_sites(
    db: AsyncSession,
    site_id: str,
    limit: int = 5,
    min_similarity: float = 0.5,
) -> list[dict[str, Any]]:
    """Search for ecological twin sites."""
    twins = await search_twins(
        db, target_site_id=site_id, limit=limit, min_similarity=min_similarity
    )
    return [
        {
            "twin_site_id": t.site_b_id,
            "overall_similarity": t.overall_similarity,
            "vector_similarity": t.vector_similarity,
            "feature_similarity": t.feature_similarity,
            "match_signals": t.match_signals,
            "differentiators": t.differentiators,
        }
        for t in twins
    ]


async def tool_compare_sites(
    db: AsyncSession,
    site_a_id: str,
    site_b_id: str,
) -> dict[str, Any] | None:
    """Perform side-by-side differential analysis of two stream sites."""
    p_a = (
        await db.execute(select(StreamProfile).where(StreamProfile.site_id == site_a_id))
    ).scalar_one_or_none()
    p_b = (
        await db.execute(select(StreamProfile).where(StreamProfile.site_id == site_b_id))
    ).scalar_one_or_none()
    if not p_a or not p_b:
        return None

    # Calculate similarity
    sim = calculate_twin_similarity(
        site_a_id=site_a_id,
        profile_a=p_a,
        vector_a=p_a.embedding.vector if p_a.embedding else [],
        site_b_id=site_b_id,
        profile_b=p_b,
        vector_b=p_b.embedding.vector if p_b.embedding else [],
    )

    return {
        "site_a_id": site_a_id,
        "site_b_id": site_b_id,
        "overall_similarity": sim.overall_similarity,
        "match_signals": sim.match_signals,
        "differentiators": sim.differentiators,
    }


async def tool_get_evidence(
    db: AsyncSession,
    site_id: str,
    node_type: str | None = None,
) -> dict[str, Any]:
    """Extract relational evidence graph nodes and edges for a site."""
    graph = await build_evidence_graph_for_site(db, site_id, persist=False)
    nodes = graph["nodes"]
    edges = graph["edges"]
    if node_type:
        nodes = [n for n in nodes if n.node_type == node_type.upper()]

    return {
        "site_id": site_id,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "contradictions": [
            {
                "edge_id": e.id,
                "source": e.source_node_id,
                "target": e.target_node_id,
                "reason": e.reason,
            }
            for e in edges
            if e.edge_type == "contradicts"
        ],
        "supports": [
            {
                "edge_id": e.id,
                "source": e.source_node_id,
                "target": e.target_node_id,
                "reason": e.reason,
            }
            for e in edges
            if e.edge_type == "supports"
        ],
    }


async def tool_find_corroborating_evidence(
    db: AsyncSession,
    observation_id: str,
) -> dict[str, Any]:
    """Find supporting or contradicting telemetry for an observation."""
    obs_res = await db.execute(select(Observation).where(Observation.id == observation_id))
    obs = obs_res.scalar_one_or_none()
    if not obs:
        return {"error": f"Observation {observation_id} not found"}

    graph = await build_evidence_graph_for_site(db, obs.site_id, persist=False)
    obs_node_id = f"node:obs:{obs.id}"

    supporting = [
        e.reason
        for e in graph["edges"]
        if e.source_node_id == obs_node_id and e.edge_type == "supports"
    ]
    contradicting = [
        e.reason
        for e in graph["edges"]
        if e.source_node_id == obs_node_id and e.edge_type == "contradicts"
    ]

    return {
        "observation_id": observation_id,
        "site_id": obs.site_id,
        "corroborated": len(supporting) > 0 and len(contradicting) == 0,
        "supporting_reasons": supporting,
        "contradicting_reasons": contradicting,
    }


async def tool_get_interventions(
    db: AsyncSession,
    site_id: str,
) -> list[dict[str, Any]]:
    """Suggest targeted ecological restoration interventions based on site gaps."""
    p_res = await db.execute(select(StreamProfile).where(StreamProfile.site_id == site_id))
    profile = p_res.scalar_one_or_none()
    if not profile:
        return []

    interventions = []
    if (profile.vegetation_score or 100) < 60:
        interventions.append(
            {
                "type": "riparian_buffer",
                "title": "Native Riparian Buffer Planting",
                "description": "Establish a 15m native buffer zone with Alnus glutinosa and Salix alba to reduce thermal stress and filter runoff.",
                "target_dimension": "vegetation_score",
                "expected_gain": "+25 points",
            }
        )
    if (profile.water_quality_score or 100) < 60:
        interventions.append(
            {
                "type": "stormwater_wetland",
                "title": "Constructed Stormwater Bio-Retention Swale",
                "description": "Install bio-filtration cells upstream to intercept nutrient surges and reduce turbidity spikes.",
                "target_dimension": "water_quality_score",
                "expected_gain": "+30 points",
            }
        )
    if (profile.hydromorphology_score or 100) < 60:
        interventions.append(
            {
                "type": "large_woody_debris",
                "title": "In-Stream Deflector & Woody Debris Installation",
                "description": "Place structured wood elements to create pool-riffle sequences and oxygenate slow-moving reaches.",
                "target_dimension": "hydromorphology_score",
                "expected_gain": "+20 points",
            }
        )
    return interventions


async def tool_calculate_information_gain(
    db: AsyncSession,
    site_id: str,
    proposed_dimension: str,
) -> dict[str, Any]:
    """Calculate expected information gain from collecting data on a specific dimension."""
    p_res = await db.execute(select(StreamProfile).where(StreamProfile.site_id == site_id))
    profile = p_res.scalar_one_or_none()

    curr_cov = profile.data_coverage_pct if profile else 0.0
    dim_status = (
        profile.dimension_status.get(proposed_dimension, "missing") if profile else "missing"
    )

    if dim_status == "missing":
        gain = 0.35
        rationale = f"Dimension '{proposed_dimension}' is entirely missing. Observing it closes an epistemic void."
    elif dim_status == "estimated":
        gain = 0.20
        rationale = f"Dimension '{proposed_dimension}' is estimated from EO; ground truth yields high validation gain."
    else:
        gain = 0.05
        rationale = f"Dimension '{proposed_dimension}' is already observed; repeated sampling adds temporal stability."

    return {
        "site_id": site_id,
        "proposed_dimension": proposed_dimension,
        "current_status": dim_status,
        "current_coverage_pct": curr_cov,
        "expected_information_gain": gain,
        "rationale": rationale,
    }
