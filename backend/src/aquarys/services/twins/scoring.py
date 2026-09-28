"""Twin scoring engine evaluating multi-dimensional similarity between stream sites."""

import math

from aquarys.models import StreamProfile, StreamSimilarity


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2, strict=False))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def calculate_twin_similarity(
    site_a_id: str,
    profile_a: StreamProfile,
    vector_a: list[float],
    site_b_id: str,
    profile_b: StreamProfile,
    vector_b: list[float],
) -> StreamSimilarity:
    """Calculate trust-aware similarity between two stream profiles."""

    # 1. Vector Similarity
    vec_sim = cosine_similarity(vector_a, vector_b)

    # 2. Feature Similarity (Euclidean distance on 0-100 scales)
    dimensions = [
        "water_quality_score",
        "habitat_score",
        "vegetation_score",
        "hydromorphology_score",
        "biotics_score",
        "nutrients_score",
        "eo_context_score",
        "citizen_evidence_score",
        "climate_context_score",
    ]

    feature_diffs = []
    match_signals = {}
    differentiators = []

    shared_dimensions = 0
    for dim in dimensions:
        val_a = getattr(profile_a, dim)
        val_b = getattr(profile_b, dim)

        if val_a is not None and val_b is not None:
            shared_dimensions += 1
            diff = abs(val_a - val_b)
            feature_diffs.append(diff)

            # Generate explainability signals
            dim_name = dim.replace("_score", "").replace("_", " ").title()
            if diff <= 10.0:
                match_signals[dim] = f"Highly aligned {dim_name} (Δ{diff:.1f})"
            elif diff > 30.0:
                higher = site_a_id if val_a > val_b else site_b_id
                differentiators.append(f"{higher} has significantly higher {dim_name}")

    if feature_diffs:
        # Max diff is 100 per dimension. Convert mean diff to 0.0-1.0 similarity
        mean_diff = sum(feature_diffs) / len(feature_diffs)
        feat_sim = max(0.0, 1.0 - (mean_diff / 100.0))
    else:
        feat_sim = 0.0

    # 3. Data Coverage & Temporal
    # Penalize if they share very few dimensions
    data_coverage = shared_dimensions / len(dimensions)

    # Temporal alignment (assume profiles are updated closely, can be refined)
    temporal_alignment = 1.0
    if profile_a.updated_at and profile_b.updated_at:
        days_diff = abs((profile_a.updated_at - profile_b.updated_at).total_seconds()) / 86400
        temporal_alignment = max(0.0, 1.0 - (days_diff / 365.0))  # Decay over a year

    # 4. Evidence Confidence
    evidence_conf = (profile_a.evidence_confidence_pct + profile_b.evidence_confidence_pct) / 200.0

    # 5. Overall Combine
    # Vector: 40%, Feature: 40%, Evidence/Coverage penalty
    base_sim = (vec_sim * 0.4) + (feat_sim * 0.6)

    # Penalty for low overlap or low confidence
    overall_similarity = base_sim * (0.8 + 0.2 * data_coverage) * (0.9 + 0.1 * evidence_conf)
    overall_similarity = max(0.0, min(1.0, overall_similarity))

    return StreamSimilarity(
        id=f"{site_a_id}_{site_b_id}",
        site_a_id=site_a_id,
        site_b_id=site_b_id,
        overall_similarity=round(overall_similarity, 3),
        vector_similarity=round(vec_sim, 3),
        feature_similarity=round(feat_sim, 3),
        temporal_alignment=round(temporal_alignment, 3),
        data_coverage=round(data_coverage, 3),
        evidence_confidence=round(evidence_conf, 3),
        match_signals=match_signals,
        differentiators=differentiators,
    )
