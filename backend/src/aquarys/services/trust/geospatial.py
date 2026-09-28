"""Geospatial validity evaluator for observation trust assessment."""

import math
from typing import Any


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on the earth in km."""
    radius_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def evaluate_geospatial(
    observation_data: dict[str, Any],
    site_data: dict[str, Any] | None = None,
) -> tuple[float, list[str], list[str]]:
    """
    Evaluates geospatial plausibility and proximity to designated monitoring site.
    Returns: (score, positive_signals, negative_signals)
    """
    score = 1.0
    positive_signals = []
    negative_signals = []

    obs_lat = observation_data.get("latitude")
    obs_lon = observation_data.get("longitude")

    if obs_lat is None or obs_lon is None:
        return 0.0, [], ["Missing coordinate location"]

    obs_lat = float(obs_lat)
    obs_lon = float(obs_lon)

    # Global bounds check
    if not (-90.0 <= obs_lat <= 90.0 and -180.0 <= obs_lon <= 180.0):
        return 0.0, [], ["Coordinates out of planetary physical bounds"]

    # Site proximity check if site data is available
    if site_data:
        site_lat = site_data.get("latitude")
        site_lon = site_data.get("longitude")

        if site_lat is not None and site_lon is not None:
            dist_km = haversine_distance_km(obs_lat, obs_lon, float(site_lat), float(site_lon))
            if dist_km <= 0.1:
                positive_signals.append(
                    f"Precise site proximity ({round(dist_km * 1000, 1)}m from site centroid)"
                )
            elif dist_km <= 0.5:
                positive_signals.append(f"Within site reach corridor ({round(dist_km * 1000, 1)}m)")
            elif dist_km <= 2.0:
                score -= 0.15
                negative_signals.append(
                    f"Moderate distance from registered site ({round(dist_km, 2)}km)"
                )
            else:
                score -= 0.4
                negative_signals.append(
                    f"Significant spatial offset from site ({round(dist_km, 2)}km)"
                )

    # Null Island check (0.0, 0.0)
    if abs(obs_lat) < 0.001 and abs(obs_lon) < 0.001:
        score -= 0.9
        negative_signals.append("Near-zero coordinate anomaly (Null Island artifact)")
    else:
        positive_signals.append("Valid non-zero coordinates")

    score = max(0.0, min(1.0, score))
    return round(score, 3), positive_signals, negative_signals
