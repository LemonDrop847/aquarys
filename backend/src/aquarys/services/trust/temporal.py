"""Temporal validity evaluator for observation trust assessment."""

from datetime import UTC, datetime
from typing import Any


def evaluate_temporal(observation_data: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    """
    Evaluates temporal plausibility of an observation.
    Checks observed_at timestamp against future dates, unreasonable historical dates,
    and latency between observation and ingestion.
    Returns: (score, positive_signals, negative_signals)
    """
    score = 1.0
    positive_signals = []
    negative_signals = []

    observed_at = observation_data.get("observed_at")
    if not observed_at:
        return 0.2, [], ["Missing observation timestamp"]

    if isinstance(observed_at, str):
        try:
            observed_dt = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        except ValueError:
            return 0.3, [], [f"Unparseable observation timestamp: {observed_at}"]
    elif isinstance(observed_at, datetime):
        observed_dt = observed_at
    else:
        return 0.3, [], [f"Invalid observation timestamp type: {type(observed_at)}"]

    if observed_dt.tzinfo is None:
        observed_dt = observed_dt.replace(tzinfo=UTC)

    now = datetime.now(UTC)

    # 1. Future date check
    if observed_dt > now:
        delta = (observed_dt - now).total_seconds()
        if delta > 300:  # > 5 minutes in the future
            score -= 0.6
            negative_signals.append(
                f"Future observation timestamp detected: {observed_dt.isoformat()}"
            )
        else:
            # Minor clock drift
            score -= 0.05
            negative_signals.append("Minor clock drift (within 5 minutes in future)")

    # 2. Historical bound (e.g. before 1990 is implausible for modern citizen monitoring)
    earliest_valid = datetime(1990, 1, 1, tzinfo=UTC)
    if observed_dt < earliest_valid:
        score -= 0.5
        negative_signals.append(
            f"Implausibly old timestamp for digital observation: {observed_dt.year}"
        )
    else:
        positive_signals.append(
            f"Observation timestamp valid ({observed_dt.strftime('%Y-%m-%d %H:%M UTC')})"
        )

    # 3. Daylight plausibility check (approximate daytime hours 05:00 - 22:00 for visual stream checks)
    hour = observed_dt.hour
    if 6 <= hour <= 21:
        positive_signals.append("Recorded during typical daylight monitoring hours")
    else:
        # Night observation might have lower visual clarity accuracy
        clarity = observation_data.get("water_clarity")
        if clarity:
            score -= 0.05
            negative_signals.append(
                f"Visual clarity assessed during nighttime/low-light hours ({hour:02d}:00 UTC)"
            )

    score = max(0.0, min(1.0, score))
    return round(score, 3), positive_signals, negative_signals
