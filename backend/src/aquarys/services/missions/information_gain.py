"""Information Gain and Uncertainty Reduction Engine for aquatic monitoring."""

import math
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.models import StreamProfile

# Base uncertainty weights by ecological dimension
DIMENSION_ENTROPY_WEIGHTS = {
    "macroinvertebrates": 0.90,
    "nutrients": 0.80,
    "water_quality": 0.75,
    "habitat": 0.70,
    "vegetation": 0.65,
    "hydromorphology": 0.60,
    "biotics": 0.85,
    "eo_context": 0.50,
    "citizen_evidence": 0.55,
    "climate_context": 0.40,
    "spatial_continuity": 0.65,
}

# Observation power to resolve uncertainty by survey type
OBSERVATION_POWER = {
    "macroinvertebrates": 0.75,
    "nutrients": 0.80,
    "water_quality": 0.70,
    "habitat": 0.65,
    "vegetation": 0.60,
    "hydromorphology": 0.55,
    "biotics": 0.70,
    "eo_context": 0.50,
    "spatial_continuity": 0.65,
}


async def calculate_dimension_information_gain(
    db: AsyncSession,
    site_id: str,
    dimension: str,
) -> dict[str, Any]:
    """Calculate expected epistemic entropy reduction for a target dimension at a site."""
    stmt = select(StreamProfile).where(StreamProfile.site_id == site_id)
    res = await db.execute(stmt)
    profile = res.scalar_one_or_none()

    dim_key = dimension.lower()
    base_weight = DIMENSION_ENTROPY_WEIGHTS.get(dim_key, 0.60)
    obs_power = OBSERVATION_POWER.get(dim_key, 0.60)

    # Calculate prior uncertainty based on status and coverage
    if profile:
        dim_status = (profile.dimension_status or {}).get(dim_key, "missing")
        coverage_fraction = (profile.data_coverage_pct or 0.0) / 100.0
        confidence_fraction = (profile.evidence_confidence_pct or 0.0) / 100.0

        if dim_status == "missing":
            prior_uncertainty = base_weight * 0.95
        elif dim_status == "estimated":
            prior_uncertainty = base_weight * 0.65
        elif dim_status == "derived":
            prior_uncertainty = base_weight * 0.40
        else:  # observed
            prior_uncertainty = base_weight * (
                1.0 - (confidence_fraction * 0.5 + coverage_fraction * 0.3)
            )
    else:
        # No profile available -> high uncertainty
        prior_uncertainty = base_weight * 0.90
        dim_status = "missing"

    prior_uncertainty = min(1.0, max(0.05, prior_uncertainty))

    # Calculate expected posterior uncertainty after targeted sampling
    # Expected uncertainty reduction formula: IG = U_prior - E[U_post]
    expected_posterior_uncertainty = prior_uncertainty * (1.0 - obs_power)
    expected_information_gain = round(prior_uncertainty - expected_posterior_uncertainty, 4)

    # Calculate Shannon Entropy representation
    p = max(0.01, min(0.99, prior_uncertainty))
    prior_shannon_entropy = round(-(p * math.log2(p) + (1 - p) * math.log2(1 - p)), 3)

    return {
        "site_id": site_id,
        "dimension": dimension,
        "dimension_status": dim_status,
        "prior_uncertainty": round(prior_uncertainty, 4),
        "expected_posterior_uncertainty": round(expected_posterior_uncertainty, 4),
        "expected_information_gain": expected_information_gain,
        "prior_shannon_entropy": prior_shannon_entropy,
        "observation_resolving_power": obs_power,
        "reasoning": (
            f"Sampling {dimension} addresses a {dim_status} dimension with prior uncertainty of "
            f"{prior_uncertainty:.2f}, yielding expected information gain of {expected_information_gain:.2f}."
        ),
    }
