"""Knowledge Gap Detection Engine for urban stream monitoring sites."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.models import (
    EOMeasurement,
    Measurement,
    Observation,
    Site,
    StreamProfile,
)

CRITICAL_DIMENSIONS = {
    "macroinvertebrates": 0.85,
    "nutrients": 0.75,
    "water_quality": 0.80,
    "habitat": 0.70,
    "vegetation": 0.65,
    "hydromorphology": 0.60,
    "biotics": 0.85,
    "eo_context": 0.50,
    "citizen_evidence": 0.55,
    "climate_context": 0.40,
}


async def detect_knowledge_gaps(db: AsyncSession, site_id: str) -> list[dict[str, Any]]:
    """Analyze site telemetry, profile status, and spatial coverage to identify epistemic data voids."""
    gaps: list[dict[str, Any]] = []

    # Fetch site
    site_stmt = select(Site).where(Site.id == site_id)
    site_res = await db.execute(site_stmt)
    site = site_res.scalar_one_or_none()
    if not site:
        return gaps

    # Fetch profile
    prof_stmt = select(StreamProfile).where(StreamProfile.site_id == site_id)
    prof_res = await db.execute(prof_stmt)
    profile = prof_res.scalar_one_or_none()

    # Fetch observations and measurements
    obs_stmt = select(Observation).where(Observation.site_id == site_id)
    obs_res = await db.execute(obs_stmt)
    observations = obs_res.scalars().all()

    meas_stmt = select(Measurement).where(Measurement.site_id == site_id)
    meas_res = await db.execute(meas_stmt)
    measurements = meas_res.scalars().all()

    eo_stmt = select(EOMeasurement).where(EOMeasurement.site_id == site_id)
    eo_res = await db.execute(eo_stmt)
    eo_records = eo_res.scalars().all()

    measured_parameters = {m.parameter.lower() for m in measurements if m.parameter}

    # 1. Profile dimension status checks
    dim_status = profile.dimension_status if profile and profile.dimension_status else {}

    # Check macroinvertebrates / biotics
    if (
        dim_status.get("macroinvertebrates") in ("missing", None)
        or "macroinvertebrates" not in measured_parameters
    ):
        gaps.append(
            {
                "dimension": "macroinvertebrates",
                "gap_type": "MISSING_DIMENSION",
                "severity": CRITICAL_DIMENSIONS.get("macroinvertebrates", 0.85),
                "status": dim_status.get("macroinvertebrates", "missing"),
                "reason": "Absence of biological macroinvertebrate sampling (e.g. BMWP/ASPT bio-indicators).",
                "recommended_action": "Deploy kick-net or benthic sampling upstream and downstream of reach.",
                "suggested_task_type": "Benthic Macroinvertebrate Survey",
                "priority": "HIGH",
                "suggested_offset_km": 0.15,
            }
        )

    # Check nutrients
    if dim_status.get("nutrients") in ("missing", "estimated") or not (
        {"nitrate", "phosphate", "ammonium"} & measured_parameters
    ):
        gaps.append(
            {
                "dimension": "nutrients",
                "gap_type": "ESTIMATED_OR_MISSING",
                "severity": CRITICAL_DIMENSIONS.get("nutrients", 0.75),
                "status": dim_status.get("nutrients", "missing"),
                "reason": "Nutrient loading (Nitrates/Phosphates) has not been verified with in-situ colorimetric tests.",
                "recommended_action": "Perform colorimetric nutrient strip and photometer tests.",
                "suggested_task_type": "Nutrient Chemical Assays",
                "priority": "HIGH",
                "suggested_offset_km": 0.0,
            }
        )

    # Check habitat and riparian structure
    has_vegetation_obs = any(
        o.canopy_cover_pct is not None or o.algae_coverage_pct is not None for o in observations
    )
    if not has_vegetation_obs or dim_status.get("vegetation") in ("missing", "estimated"):
        gaps.append(
            {
                "dimension": "vegetation",
                "gap_type": "UNVERIFIED_RIPARIAN",
                "severity": CRITICAL_DIMENSIONS.get("vegetation", 0.65),
                "status": dim_status.get("vegetation", "missing"),
                "reason": "Riparian buffer width, canopy cover shading, and bank vegetation are unconfirmed.",
                "recommended_action": "Survey riparian canopy cover and bank stability index.",
                "suggested_task_type": "Riparian Habitat & Canopy Assessment",
                "priority": "MEDIUM",
                "suggested_offset_km": -0.20,  # Upstream
            }
        )

    # Check hydromorphology
    has_flow_obs = any(o.flow_rate_category or o.water_clarity for o in observations)
    if not has_flow_obs or dim_status.get("hydromorphology") in ("missing", "estimated"):
        gaps.append(
            {
                "dimension": "hydromorphology",
                "gap_type": "MISSING_FLOW_DATA",
                "severity": CRITICAL_DIMENSIONS.get("hydromorphology", 0.60),
                "status": dim_status.get("hydromorphology", "missing"),
                "reason": "Stream cross-section morphology, flow velocity, and culvert obstruction lack ground truth.",
                "recommended_action": "Record flow velocity float tests and channel cross-section measurements.",
                "suggested_task_type": "Hydromorphological Flow & Depth Profiling",
                "priority": "MEDIUM",
                "suggested_offset_km": 0.25,  # Downstream
            }
        )

    # 2. Upstream / Downstream Void Detection
    if len(observations) < 3:
        gaps.append(
            {
                "dimension": "spatial_continuity",
                "gap_type": "SPATIAL_VOID",
                "severity": 0.70,
                "status": "sparse_coverage",
                "reason": "Insufficient spatial density of citizen observations along the longitudinal stream reach.",
                "recommended_action": "Establish synchronous multi-point visual and sensory logging stations.",
                "suggested_task_type": "Longitudinal Reach Observational Sweep",
                "priority": "HIGH",
                "suggested_offset_km": -0.35,  # Upstream void
            }
        )

    # 3. Satellite validation void
    if not eo_records:
        gaps.append(
            {
                "dimension": "eo_context",
                "gap_type": "MISSING_EARTH_OBSERVATION",
                "severity": 0.50,
                "status": "missing",
                "reason": "Sentinel-2 / Landsat optical and thermal telemetry not aligned for current epoch.",
                "recommended_action": "Correlate local ground albedo and canopy density with Sentinel-2 NDVI.",
                "suggested_task_type": "Ground-Truth EO Validation",
                "priority": "LOW",
                "suggested_offset_km": 0.0,
            }
        )

    return gaps
