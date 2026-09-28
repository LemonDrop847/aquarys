"""Stream fingerprint builder — 9-dimension ecological scoring + deterministic embedding."""

import math
from typing import Any

_DIMENSIONS = [
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

# Mapping flow_rate_category to numeric health proxy (0-100, higher = healthier natural flow)
_FLOW_SCORE = {
    "dry": 10,
    "stagnant": 25,
    "slow": 50,
    "moderate": 80,
    "fast": 70,
    "torrential": 40,
}

# Water clarity quality proxy
_CLARITY_SCORE = {
    "crystal_clear": 95,
    "clear": 85,
    "slightly_turbid": 55,
    "turbid": 30,
    "cloudy": 20,
    "foamy": 10,
}

# Odor severity (inverse: lower number = worse)
_ODOR_SCORE = {
    "none": 100,
    "earthy": 80,
    "musty": 60,
    "chemical": 20,
    "sewage": 10,
    "rotten_eggs": 5,
}


def _clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, val))


def _safe_mean(vals: list[float]) -> float | None:
    return sum(vals) / len(vals) if vals else None


def build_fingerprint(
    site_data: dict[str, Any],
    observations: list[dict[str, Any]] | None = None,
    measurements: list[dict[str, Any]] | None = None,
    eo_data: list[dict[str, Any]] | None = None,
    trust_scores: list[float] | None = None,
) -> dict[str, Any]:
    """
    Build 9-dimension ecological fingerprint from raw dicts.

    Tracks missing vs zero explicitly via dimension_status.
    Returns scores dict + embedding vector.
    """
    observations = observations or []
    measurements = measurements or []
    eo_data = eo_data or []

    scores: dict[str, float | None] = {d: None for d in _DIMENSIONS}
    status: dict[str, str] = {d: "missing" for d in _DIMENSIONS}

    # --- 1. Water Quality (pH, DO, turbidity, conductivity) ---
    wq_components: list[float] = []
    for m in measurements:
        param = (m.get("parameter") or m.get("parameter_name") or "").lower()
        val = m.get("value")
        if val is None:
            continue
        val = float(val)
        if "ph" == param:
            # Ideal pH ~7; deviation penalized. Score 100 at 7, drops to 0 at 4 or 10
            wq_components.append(_clamp(100 - abs(val - 7.0) * 33.3))
        elif param in ("dissolved_oxygen", "do"):
            # 0-14 mg/L typical. >8 good, <4 bad
            wq_components.append(_clamp(val / 10.0 * 100))
        elif "turbidity" in param:
            # NTU: 0 = clear, >50 = bad
            wq_components.append(_clamp(100 - val * 2))
        elif "conductivity" in param:
            # uS/cm: ~200-800 normal, >1500 stressed
            wq_components.append(_clamp(100 - max(0, val - 300) / 12))
    if wq_components:
        scores["water_quality_score"] = round(_clamp(sum(wq_components) / len(wq_components)), 2)
        status["water_quality_score"] = "observed"

    # --- 2. Habitat (canopy cover, litter presence) ---
    hab: list[float] = []
    for o in observations:
        canopy = o.get("canopy_cover_pct")
        if canopy is not None:
            # Higher canopy = healthier riparian; cap benefit at 80%
            hab.append(_clamp(float(canopy) * 1.25))
        litter = o.get("litter_present")
        if litter is not None:
            hab.append(20.0 if litter else 90.0)
    if hab:
        scores["habitat_score"] = round(_clamp(sum(hab) / len(hab)), 2)
        status["habitat_score"] = "observed"

    # --- 3. Vegetation (NDVI from EO + algae coverage from obs) ---
    veg: list[float] = []
    for eo in eo_data:
        ndvi = eo.get("ndvi")
        if ndvi is not None:
            # NDVI [-1,1] -> score. 0.6+ is lush, <0.1 is bare
            veg.append(_clamp((float(ndvi) + 0.1) / 0.8 * 100))
    for o in observations:
        algae = o.get("algae_coverage_pct")
        if algae is not None:
            # High algae = eutrophication = bad vegetation health
            veg.append(_clamp(100 - float(algae)))
    if veg:
        scores["vegetation_score"] = round(_clamp(sum(veg) / len(veg)), 2)
        status["vegetation_score"] = "observed"

    # --- 4. Hydromorphology (flow rate + clarity) ---
    hydro: list[float] = []
    for o in observations:
        flow = o.get("flow_rate_category")
        if flow and flow in _FLOW_SCORE:
            hydro.append(float(_FLOW_SCORE[flow]))
        clarity = o.get("water_clarity")
        if clarity and clarity in _CLARITY_SCORE:
            hydro.append(float(_CLARITY_SCORE[clarity]))
    if hydro:
        scores["hydromorphology_score"] = round(_clamp(sum(hydro) / len(hydro)), 2)
        status["hydromorphology_score"] = "observed"

    # --- 5. Biotics (odor, algae, litter — biotic stress indicators) ---
    bio: list[float] = []
    for o in observations:
        odor = o.get("odor")
        if odor and odor in _ODOR_SCORE:
            bio.append(float(_ODOR_SCORE[odor]))
        algae = o.get("algae_coverage_pct")
        if algae is not None:
            bio.append(_clamp(100 - float(algae) * 1.5))
    if bio:
        scores["biotics_score"] = round(_clamp(sum(bio) / len(bio)), 2)
        status["biotics_score"] = "observed"

    # --- 6. Nutrients (nitrate, phosphate from measurements) ---
    nut: list[float] = []
    for m in measurements:
        param = (m.get("parameter") or m.get("parameter_name") or "").lower()
        val = m.get("value")
        if val is None:
            continue
        val = float(val)
        if "nitrate" in param:
            # mg/L: <1 pristine, >10 impaired
            nut.append(_clamp(100 - val * 10))
        elif "phosphate" in param or "phosphorus" in param:
            # mg/L: <0.1 pristine, >0.5 impaired
            nut.append(_clamp(100 - val * 200))
    if nut:
        scores["nutrients_score"] = round(_clamp(sum(nut) / len(nut)), 2)
        status["nutrients_score"] = "observed"

    # --- 7. EO Context (NDWI, cloud cover, resolution) ---
    eo_ctx: list[float] = []
    for eo in eo_data:
        ndwi = eo.get("ndwi")
        if ndwi is not None:
            # NDWI > 0 = water present; higher = more water
            eo_ctx.append(_clamp(float(ndwi) * 100 + 50))
        cloud = eo.get("cloud_cover_pct")
        if cloud is not None:
            # Lower cloud = better data quality
            eo_ctx.append(_clamp(100 - float(cloud)))
    if eo_ctx:
        scores["eo_context_score"] = round(_clamp(sum(eo_ctx) / len(eo_ctx)), 2)
        status["eo_context_score"] = "observed"

    # --- 8. Citizen Evidence (observation count, frequency, image coverage) ---
    if observations:
        obs_count = len(observations)
        img_count = sum(1 for o in observations if o.get("image_urls"))
        count_score = min(100.0, obs_count * 10.0)  # 10+ obs = max
        img_ratio = (img_count / obs_count * 100.0) if obs_count else 0.0
        scores["citizen_evidence_score"] = round(_clamp((count_score + img_ratio) / 2), 2)
        status["citizen_evidence_score"] = "observed"

    # --- 9. Climate Context (surface temp from EO) ---
    temps: list[float] = []
    for eo in eo_data:
        temp = eo.get("surface_temp_c")
        if temp is not None:
            temps.append(float(temp))
    if temps:
        avg_temp = sum(temps) / len(temps)
        # Normalize: 10-25°C is typical healthy range. Score drops outside
        scores["climate_context_score"] = round(_clamp(100 - abs(avg_temp - 17.5) * 5), 2)
        status["climate_context_score"] = "observed"

    # --- Data Coverage ---
    scored = [v for v in scores.values() if v is not None]
    data_coverage = (len(scored) / len(_DIMENSIONS)) * 100.0

    # --- Evidence Confidence ---
    evidence_confidence = 0.0
    if trust_scores:
        evidence_confidence = sum(trust_scores) / len(trust_scores) * 100.0

    return {
        **scores,
        "dimension_status": status,
        "data_coverage_pct": round(data_coverage, 2),
        "evidence_confidence_pct": round(evidence_confidence, 2),
    }


def build_embedding(fingerprint: dict[str, Any], version: str = "v1-deterministic") -> list[float]:
    """
    Deterministic 18-dim embedding from fingerprint.

    For each of 9 dimensions: [normalized_score, has_data_flag].
    Missing dimensions get [0.0, 0.0] — distinguishing missing from zero (which would be [0.0, 1.0]).
    """
    vector: list[float] = []
    for dim in _DIMENSIONS:
        val = fingerprint.get(dim)
        if val is not None:
            vector.append(val / 100.0)  # Normalize to [0, 1]
            vector.append(1.0)  # Data present flag
        else:
            vector.append(0.0)
            vector.append(0.0)  # Missing flag
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors. Returns 0.0 if either is zero-length."""
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
