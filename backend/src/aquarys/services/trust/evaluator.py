"""Master trust evaluation service orchestrating multi-dimensional evidence assessment."""

from typing import Any

from pydantic import BaseModel, Field

from aquarys.services.trust.completeness import evaluate_completeness
from aquarys.services.trust.consistency import evaluate_consistency
from aquarys.services.trust.corroboration import evaluate_corroboration
from aquarys.services.trust.duplicate import evaluate_duplicate_risk
from aquarys.services.trust.geospatial import evaluate_geospatial
from aquarys.services.trust.temporal import evaluate_temporal


class EvidenceProfile(BaseModel):
    """Normalized evidence confidence profile for an observation."""

    completeness: float = Field(ge=0.0, le=1.0)
    consistency: float = Field(ge=0.0, le=1.0)
    location: float = Field(ge=0.0, le=1.0)
    temporal_validity: float = Field(ge=0.0, le=1.0)
    duplicate_risk: float = Field(ge=0.0, le=1.0)
    image_support: float = Field(ge=0.0, le=1.0)
    cross_observer: float = Field(ge=0.0, le=1.0)
    independent_support: float = Field(ge=0.0, le=1.0)
    overall_confidence: float = Field(ge=0.0, le=1.0)
    flags: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)


def evaluate_observation_trust(
    observation_data: dict[str, Any],
    site_data: dict[str, Any] | None = None,
    existing_observations: list[dict[str, Any]] | None = None,
    measurements: list[dict[str, Any]] | None = None,
    eo_data: list[dict[str, Any]] | None = None,
) -> EvidenceProfile:
    """
    Evaluates evidence quality and trust score across 8 dimensions.
    Deterministic for identical input data.
    """
    all_positive = []
    all_negative = []

    # 1. Completeness
    completeness_score, comp_pos, comp_neg = evaluate_completeness(observation_data)
    all_positive.extend(comp_pos)
    all_negative.extend(comp_neg)

    # 2. Consistency
    consistency_score, cons_pos, cons_neg = evaluate_consistency(observation_data)
    all_positive.extend(cons_pos)
    all_negative.extend(cons_neg)

    # 3. Geospatial validity
    location_score, geo_pos, geo_neg = evaluate_geospatial(observation_data, site_data)
    all_positive.extend(geo_pos)
    all_negative.extend(geo_neg)

    # 4. Temporal validity
    temporal_score, temp_pos, temp_neg = evaluate_temporal(observation_data)
    all_positive.extend(temp_pos)
    all_negative.extend(temp_neg)

    # 5. Duplicate risk
    dup_risk_score, dup_pos, dup_neg = evaluate_duplicate_risk(
        observation_data, existing_observations
    )
    all_positive.extend(dup_pos)
    all_negative.extend(dup_neg)

    # 6. Image support (based on photo attachments and metadata)
    images = observation_data.get("image_urls") or []
    if len(images) > 2:
        image_support_score = 0.95
        all_positive.append(f"Multiple ({len(images)}) photographic evidence records")
    elif len(images) > 0:
        image_support_score = 0.80
        all_positive.append("Single photographic evidence record")
    else:
        image_support_score = 0.35
        all_negative.append("Lacks photographic verification")

    # 7 & 8. Corroboration (Cross-observer and Independent sensor/EO)
    cross_observer_score, indep_score, corr_pos, corr_neg = evaluate_corroboration(
        observation_data,
        other_observations=existing_observations,
        measurements=measurements,
        eo_data=eo_data,
    )
    all_positive.extend(corr_pos)
    all_negative.extend(corr_neg)

    # Overall Confidence Calculation
    # Weights for evidence synthesis:
    # Completeness: 15%, Consistency: 20%, Location: 15%, Temporal: 10%, Image: 15%, Cross: 10%, Indep: 15%
    # Penalized by duplicate risk
    unpenalized_confidence = (
        completeness_score * 0.15
        + consistency_score * 0.20
        + location_score * 0.15
        + temporal_score * 0.10
        + image_support_score * 0.15
        + cross_observer_score * 0.10
        + indep_score * 0.15
    )

    # High duplicate risk sharply degrades confidence
    overall_confidence = unpenalized_confidence * (1.0 - (dup_risk_score * 0.7))
    overall_confidence = max(0.0, min(1.0, overall_confidence))

    # Construct alert flags
    flags = []
    if completeness_score < 0.5:
        flags.append("LOW_COMPLETENESS")
    if consistency_score < 0.6:
        flags.append("ECOLOGICAL_INCONSISTENCY")
    if location_score < 0.6:
        flags.append("SPATIAL_OFFSET")
    if temporal_score < 0.6:
        flags.append("TEMPORAL_ANOMALY")
    if dup_risk_score > 0.6:
        flags.append("DUPLICATE_SUSPECT")
    if image_support_score < 0.4:
        flags.append("UNVERIFIED_VISUAL")

    return EvidenceProfile(
        completeness=round(completeness_score, 3),
        consistency=round(consistency_score, 3),
        location=round(location_score, 3),
        temporal_validity=round(temporal_score, 3),
        duplicate_risk=round(dup_risk_score, 3),
        image_support=round(image_support_score, 3),
        cross_observer=round(cross_observer_score, 3),
        independent_support=round(indep_score, 3),
        overall_confidence=round(overall_confidence, 3),
        flags=flags,
        positive_signals=all_positive,
        negative_signals=all_negative,
    )
