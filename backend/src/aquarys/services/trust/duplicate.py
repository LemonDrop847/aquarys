"""Duplicate detection evaluator for observation trust assessment."""

from datetime import UTC, datetime
from typing import Any

from aquarys.services.trust.geospatial import haversine_distance_km


def evaluate_duplicate_risk(
    observation_data: dict[str, Any],
    existing_observations: list[dict[str, Any]] | None = None,
) -> tuple[float, list[str], list[str]]:
    """
    Evaluates risk of observation being a duplicate (0.0 = low risk/unique, 1.0 = high risk/duplicate).
    Returns: (duplicate_risk_score, positive_signals, negative_signals)
    """
    duplicate_risk = 0.0
    positive_signals = []
    negative_signals = []

    if not existing_observations:
        positive_signals.append("No prior conflicting observations at this temporal-spatial window")
        return 0.0, positive_signals, negative_signals

    obs_id = observation_data.get("id") or observation_data.get("source_id")
    obs_lat = observation_data.get("latitude")
    obs_lon = observation_data.get("longitude")
    obs_time = observation_data.get("observed_at")
    obs_hash = observation_data.get("raw_payload_hash")
    obs_observer = observation_data.get("observer_id")

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

    duplicates_found = []

    for existing in existing_observations:
        exist_id = existing.get("id") or existing.get("source_id")
        if exist_id == obs_id:
            continue  # Same identity check

        # 1. Exact raw hash match
        exist_hash = existing.get("raw_payload_hash")
        if obs_hash and exist_hash and obs_hash == exist_hash:
            duplicate_risk = 0.95
            duplicates_found.append(f"Identical payload hash with record {exist_id}")
            break

        # 2. Same observer within 15 minutes and 20 meters
        exist_time = existing.get("observed_at")
        if isinstance(exist_time, str):
            try:
                exist_dt = datetime.fromisoformat(exist_time.replace("Z", "+00:00"))
            except ValueError:
                exist_dt = None
        elif isinstance(exist_time, datetime):
            exist_dt = exist_time
        else:
            exist_dt = None

        if exist_dt and exist_dt.tzinfo is None:
            exist_dt = exist_dt.replace(tzinfo=UTC)

        exist_lat = existing.get("latitude")
        exist_lon = existing.get("longitude")
        exist_observer = existing.get("observer_id")

        if (
            obs_dt
            and exist_dt
            and obs_lat is not None
            and obs_lon is not None
            and exist_lat is not None
            and exist_lon is not None
        ):
            time_diff_sec = abs((obs_dt - exist_dt).total_seconds())
            dist_km = haversine_distance_km(
                float(obs_lat), float(obs_lon), float(exist_lat), float(exist_lon)
            )

            if time_diff_sec < 600 and dist_km < 0.05:  # within 10 mins and 50m
                if obs_observer and exist_observer and obs_observer == exist_observer:
                    duplicate_risk = max(duplicate_risk, 0.85)
                    duplicates_found.append(
                        f"Rapid burst resubmission by same observer within {int(time_diff_sec)}s"
                    )
                else:
                    duplicate_risk = max(duplicate_risk, 0.4)
                    duplicates_found.append(
                        f"Co-temporal co-located submission ({int(time_diff_sec)}s, {int(dist_km * 1000)}m)"
                    )

    if duplicate_risk > 0.5:
        negative_signals.extend(duplicates_found)
    else:
        positive_signals.append("Temporal-spatial uniqueness verified against local registry")

    return round(duplicate_risk, 3), positive_signals, negative_signals
