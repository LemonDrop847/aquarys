"""Corroboration evaluator for observation trust assessment."""

from datetime import UTC, datetime
from typing import Any

from aquarys.services.trust.geospatial import haversine_distance_km


def evaluate_corroboration(
    observation_data: dict[str, Any],
    other_observations: list[dict[str, Any]] | None = None,
    measurements: list[dict[str, Any]] | None = None,
    eo_data: list[dict[str, Any]] | None = None,
) -> tuple[float, float, list[str], list[str]]:
    """
    Evaluates cross-observer corroboration and independent instrument/EO support.
    Returns: (cross_observer_score, independent_support_score, positive_signals, negative_signals)
    """
    cross_observer_score = 0.5  # Neutral default if isolated
    independent_support_score = 0.5
    positive_signals = []
    negative_signals = []

    obs_id = observation_data.get("id") or observation_data.get("source_id")
    obs_observer = observation_data.get("observer_id")
    obs_clarity = observation_data.get("water_clarity")
    obs_algae = observation_data.get("algae_coverage_pct")
    obs_lat = observation_data.get("latitude")
    obs_lon = observation_data.get("longitude")
    obs_time = observation_data.get("observed_at")

    if isinstance(obs_time, str):
        try:
            obs_dt = datetime.fromisoformat(obs_time.replace("Z", "+00:00"))
        except ValueError:
            obs_dt = None
    elif isinstance(obs_time, datetime):
        obs_dt = obs_time
    else:
        obs_dt = None

    if obs_dt and obs_dt.tzinfo is None:
        obs_dt = obs_dt.replace(tzinfo=UTC)

    # 1. Cross-Observer Corroboration
    if other_observations and obs_dt and obs_lat is not None and obs_lon is not None:
        nearby_distinct_reports = 0
        consistent_reports = 0

        for other in other_observations:
            other_id = other.get("id") or other.get("source_id")
            if other_id == obs_id:
                continue

            other_observer = other.get("observer_id")
            if other_observer and obs_observer and other_observer == obs_observer:
                continue  # Must be different observer for independent cross-corroboration

            other_lat = other.get("latitude")
            other_lon = other.get("longitude")
            other_time = other.get("observed_at")
            if not other_lat or not other_lon or not other_time:
                continue

            if isinstance(other_time, str):
                try:
                    other_dt = datetime.fromisoformat(other_time.replace("Z", "+00:00"))
                except ValueError:
                    continue
            elif isinstance(other_time, datetime):
                other_dt = other_time
            else:
                continue

            if other_dt.tzinfo is None:
                other_dt = other_dt.replace(tzinfo=UTC)

            dist_km = haversine_distance_km(
                float(obs_lat), float(obs_lon), float(other_lat), float(other_lon)
            )
            time_diff_days = abs((obs_dt - other_dt).total_seconds()) / 86400.0

            if dist_km <= 1.0 and time_diff_days <= 3.0:
                nearby_distinct_reports += 1
                other_clarity = other.get("water_clarity")
                if obs_clarity and other_clarity and obs_clarity == other_clarity:
                    consistent_reports += 1

        if nearby_distinct_reports > 0:
            ratio = consistent_reports / nearby_distinct_reports
            cross_observer_score = min(1.0, 0.6 + ratio * 0.35)
            positive_signals.append(
                f"Cross-corroborated by {nearby_distinct_reports} independent observer report(s) ({consistent_reports} matching status)"
            )
        else:
            cross_observer_score = 0.5
            positive_signals.append(
                "Isolated observation (no concurrent secondary observer reports)"
            )
    else:
        cross_observer_score = 0.5

    # 2. Independent Sensor / EO Support
    sensor_matches = 0
    if measurements:
        for m in measurements:
            param = m.get("parameter_name") or m.get("parameter")
            val = m.get("value")
            if param and val is not None:
                # E.g. Turbidity vs Water clarity
                if "turbidity" in str(param).lower():
                    if obs_clarity in ["crystal_clear", "clear"] and float(val) < 10.0:
                        sensor_matches += 1
                        positive_signals.append(
                            f"Turbidity probe ({val} NTU) corroborates clear water assessment"
                        )
                    elif obs_clarity in ["turbid", "cloudy"] and float(val) > 15.0:
                        sensor_matches += 1
                        positive_signals.append(
                            f"Turbidity probe ({val} NTU) corroborates turbid water assessment"
                        )
                # E.g. Dissolved oxygen
                if "oxygen" in str(param).lower() or "do" == str(param).lower():
                    if float(val) < 4.0 and observation_data.get("odor") in [
                        "sewage",
                        "rotten_eggs",
                    ]:
                        sensor_matches += 1
                        positive_signals.append(
                            f"Low dissolved oxygen probe ({val} mg/L) corroborates anaerobic odor"
                        )

    if eo_data:
        for eo in eo_data:
            ndti = eo.get("ndti") or eo.get("turbidity_index")
            ndwi = eo.get("ndwi") or eo.get("water_index")
            ndvi = eo.get("ndvi") or eo.get("vegetation_index")
            if ndti is not None and obs_clarity in ["turbid", "cloudy"]:
                sensor_matches += 1
                positive_signals.append(
                    f"Satellite NDTI index ({ndti}) supports elevated surface turbidity"
                )
            if ndwi is not None and float(ndwi) > 0.1:
                sensor_matches += 1
                positive_signals.append(
                    f"Sentinel-2 NDWI ({ndwi}) confirms open water body footprint"
                )
            if (
                ndvi is not None
                and obs_algae is not None
                and float(obs_algae) > 30
                and float(ndvi) > 0.4
            ):
                sensor_matches += 1
                positive_signals.append(
                    f"Sentinel-2 NDVI ({ndvi}) corroborates high observed algal biomass ({obs_algae}%)"
                )

    if sensor_matches > 0:
        independent_support_score = min(1.0, 0.65 + 0.12 * sensor_matches)
    else:
        independent_support_score = 0.5
        positive_signals.append(
            "Baseline independent instrument alignment (no immediate sensor conflicts)"
        )

    return (
        round(cross_observer_score, 3),
        round(independent_support_score, 3),
        positive_signals,
        negative_signals,
    )
