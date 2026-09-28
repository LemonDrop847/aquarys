"""Consistency evaluator for observation trust assessment."""

from typing import Any


def evaluate_consistency(observation_data: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    """
    Evaluates internal logical and physical consistency of the observation.
    Returns: (score, positive_signals, negative_signals)
    """
    score = 1.0
    positive_signals = []
    negative_signals = []

    # 1. Coordinate range validation
    lat = observation_data.get("latitude")
    lon = observation_data.get("longitude")
    if lat is not None and not (-90.0 <= float(lat) <= 90.0):
        score -= 0.5
        negative_signals.append(f"Invalid latitude value: {lat}")
    if lon is not None and not (-180.0 <= float(lon) <= 180.0):
        score -= 0.5
        negative_signals.append(f"Invalid longitude value: {lon}")

    # 2. Percentage range validation
    algae = observation_data.get("algae_coverage_pct")
    if algae is not None:
        if not (0.0 <= float(algae) <= 100.0):
            score -= 0.3
            negative_signals.append(f"Algae coverage out of range [0, 100]: {algae}%")
        elif float(algae) <= 5.0 and observation_data.get("water_clarity") in ["cloudy", "turbid"]:
            # Plausible turbid from suspended sediment without algae
            positive_signals.append("Sediment turbidity without algal bloom detected")

    canopy = observation_data.get("canopy_cover_pct")
    if canopy is not None:
        if not (0.0 <= float(canopy) <= 100.0):
            score -= 0.3
            negative_signals.append(f"Canopy cover out of range [0, 100]: {canopy}%")

    # 3. Ecological cross-variable plausibility
    clarity = observation_data.get("water_clarity")
    if clarity == "crystal_clear" and algae is not None and float(algae) > 75.0:
        score -= 0.25
        negative_signals.append(
            f"Contradictory condition: crystal clear water with {algae}% dense algal coverage"
        )
    elif clarity == "crystal_clear" and (algae is None or float(algae) < 20.0):
        positive_signals.append("Clarity and low algal biomass logically coherent")

    flow = observation_data.get("flow_rate_category")
    odor = observation_data.get("odor")
    if flow == "fast" and odor in ["sewage", "rotten_eggs"]:
        # Fast moving water with anaerobic sewage odor is unusual unless point-source discharge
        positive_signals.append(
            "Rapid flow with distinct odor may indicate immediate active point discharge"
        )

    score = max(0.0, min(1.0, score))
    return round(score, 3), positive_signals, negative_signals
