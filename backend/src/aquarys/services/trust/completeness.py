"""Completeness evaluator for observation trust assessment."""

from typing import Any


def evaluate_completeness(observation_data: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    """
    Evaluates the completeness of an observation based on provided fields.
    Returns: (score, positive_signals, negative_signals)
    """
    essential_fields = [
        "water_clarity",
        "flow_rate_category",
        "odor",
        "algae_coverage_pct",
        "canopy_cover_pct",
        "litter_present",
    ]

    filled = 0
    missing = []

    for field in essential_fields:
        val = observation_data.get(field)
        if val is not None:
            filled += 1
        else:
            missing.append(field)

    # Base score on essential fields
    base_ratio = filled / len(essential_fields)

    # Bonus for image support and rich notes
    images = observation_data.get("image_urls") or []
    notes = observation_data.get("notes") or ""

    bonus = 0.0
    positive_signals = []
    negative_signals = []

    if len(images) > 0:
        bonus += 0.1
        positive_signals.append(f"Contains {len(images)} attached photographic evidence item(s)")
    else:
        negative_signals.append("No photographic evidence attached")

    if len(notes.strip()) > 10:
        bonus += 0.05
        positive_signals.append("Rich contextual notes provided by observer")

    score = min(1.0, base_ratio * 0.85 + bonus)

    if missing:
        negative_signals.append(f"Missing attributes: {', '.join(missing)}")
    if base_ratio >= 0.8:
        positive_signals.append("High attribute field completeness (>80%)")

    return round(score, 3), positive_signals, negative_signals
