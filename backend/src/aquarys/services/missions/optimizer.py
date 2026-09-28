"""Greedy Multi-Objective Mission Optimizer for volunteer citizen science and researcher field sweeps."""

import math
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.models import Mission, MissionTask, Site
from aquarys.services.missions.gaps import detect_knowledge_gaps
from aquarys.services.missions.information_gain import calculate_dimension_information_gain

# Degree offset per kilometer (approximate for latitude and longitude at ~38-50 deg N)
KM_TO_LAT_DEG = 1.0 / 111.0
KM_TO_LON_DEG = 1.0 / 85.0

TASK_INSTRUCTIONS = {
    "macroinvertebrates": (
        "Collect a 3-minute traveling kick-net sample in the riffle/run zone. "
        "Count and record sensitive taxa (Mayfly, Stonefly, Caddisfly) vs tolerant taxa (Tubificid worms, Chironomids) "
        "to calculate BMWP biotic index."
    ),
    "nutrients": (
        "Take a surface grab sample and dip colorimetric test strips for Nitrate (NO3-) and Nitrite (NO2-). "
        "Compare against high-precision comparator card and log results into the app."
    ),
    "vegetation": (
        "Measure canopy shading percentage using the densiometer tool. Record presence of invasive Giant Reed (Arundo donax) "
        "and estimate riparian buffer width in meters on both left and right banks."
    ),
    "hydromorphology": (
        "Conduct a 10-meter float test with an orange/cork to measure surface velocity. "
        "Measure stream wetted width and maximum water depth with the graduated wading rod."
    ),
    "spatial_continuity": (
        "Record 360-degree panoramic photos of the stream reach, log visual water clarity (turbidity tube test), "
        "and record any olfactory signatures (sulfur, sewage, hydrocarbon)."
    ),
    "eo_context": (
        "Calibrate satellite spectral ground-truth by recording surface water reflectance and canopy leaf-area index "
        "at open canopy reach coordinates."
    ),
}


async def optimize_mission(
    db: AsyncSession,
    site_id: str,
    volunteer_count: int = 5,
    available_time_minutes: int = 60,
    focus_dimensions: list[str] | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    """Optimize a field monitoring campaign to maximize epistemic information gain within time & personnel constraints."""
    # 1. Fetch site
    site_stmt = select(Site).where(Site.id == site_id)
    site_res = await db.execute(site_stmt)
    site = site_res.scalar_one_or_none()
    if not site:
        raise ValueError(f"Site {site_id} not found")

    # 2. Detect knowledge gaps
    detected_gaps = await detect_knowledge_gaps(db, site_id)

    # Filter by focus dimensions if provided
    if focus_dimensions:
        focus_set = {d.lower() for d in focus_dimensions}
        gaps_to_plan = [g for g in detected_gaps if g["dimension"].lower() in focus_set]
        # If no matching gaps, keep original detected gaps
        if not gaps_to_plan:
            gaps_to_plan = detected_gaps
    else:
        gaps_to_plan = detected_gaps

    # Sort gaps by severity descending
    gaps_to_plan.sort(key=lambda x: x.get("severity", 0.5), reverse=True)

    # 3. Calculate information gain for candidate gaps
    gap_gains: list[dict[str, Any]] = []
    for gap in gaps_to_plan:
        gain_info = await calculate_dimension_information_gain(db, site_id, gap["dimension"])
        gap_gains.append(
            {
                **gap,
                "gain_info": gain_info,
                "expected_gain": gain_info["expected_information_gain"],
            }
        )

    # Sort by expected information gain descending
    gap_gains.sort(key=lambda x: x["expected_gain"], reverse=True)

    # 4. Generate optimized task assignments
    tasks: list[dict[str, Any]] = []
    mission_id = f"mission_{uuid.uuid4().hex[:12]}"
    time_per_task = max(15, min(available_time_minutes // 2, 30))
    gaps_addressed_set: set[str] = set()

    for idx in range(volunteer_count):
        volunteer_num = idx + 1
        gap_idx = idx % len(gap_gains) if gap_gains else 0
        current_gap = (
            gap_gains[gap_idx]
            if gap_gains
            else {
                "dimension": "spatial_continuity",
                "suggested_task_type": "Longitudinal Reach Observational Sweep",
                "priority": "HIGH",
                "expected_gain": 0.35,
                "suggested_offset_km": 0.0,
            }
        )

        dimension_name = current_gap["dimension"]
        gaps_addressed_set.add(dimension_name)

        # Calculate spatial offset along longitudinal reach
        offset_km = current_gap.get("suggested_offset_km", 0.0)
        # Alternate upstream/downstream for volunteers on same gap
        offset_multiplier = 1.0 if (idx % 2 == 0) else -1.0
        final_offset_km = (offset_km if offset_km != 0 else (0.1 * (idx + 1))) * offset_multiplier

        task_lat = site.latitude + (final_offset_km * KM_TO_LAT_DEG)
        task_lon = site.longitude + (
            final_offset_km * KM_TO_LON_DEG * math.cos(math.radians(site.latitude))
        )

        # Location name
        if final_offset_km > 0.05:
            loc_name = (
                f"{site.code or site.name} Downstream (+{abs(round(final_offset_km * 1000))}m)"
            )
        elif final_offset_km < -0.05:
            loc_name = f"{site.code or site.name} Upstream (-{abs(round(final_offset_km * 1000))}m)"
        else:
            loc_name = f"{site.code or site.name} Core Reach Station"

        instructions = TASK_INSTRUCTIONS.get(
            dimension_name,
            f"Perform standard protocol monitoring and qualitative assessment for {dimension_name}.",
        )

        task_data = {
            "id": f"task_{uuid.uuid4().hex[:10]}",
            "mission_id": mission_id,
            "volunteer_index": volunteer_num,
            "volunteer_name": f"Volunteer {volunteer_num}",
            "target_location_name": loc_name,
            "latitude": round(task_lat, 6),
            "longitude": round(task_lon, 6),
            "target_observation_type": current_gap.get(
                "suggested_task_type", f"{dimension_name.title()} Sampling"
            ),
            "priority": current_gap.get("priority", "HIGH"),
            "estimated_duration_min": time_per_task,
            "expected_gain": round(
                current_gap.get("expected_gain", 0.30)
                * (0.95 ** (idx // len(gap_gains) if gap_gains else 1)),
                3,
            ),
            "instructions": instructions,
        }
        tasks.append(task_data)

    # 5. Compute aggregate mission metrics
    total_gain = sum(t["expected_gain"] for t in tasks)
    normalized_info_gain = round(min(0.98, total_gain / (1.0 + (volunteer_count * 0.2))), 3)
    coverage_improvement = round(min(65.0, len(tasks) * 12.5), 1)

    mission_record = {
        "id": mission_id,
        "title": f"Targeted Gap Reduction Campaign — {site.name}",
        "objective": (
            f"Deploy {volunteer_count} volunteers across {len(gaps_addressed_set)} critical epistemic voids "
            f"to maximize ecological fingerprint coverage and verify stream health."
        ),
        "target_site_id": site_id,
        "volunteer_count": volunteer_count,
        "available_time_minutes": available_time_minutes,
        "expected_information_gain": normalized_info_gain,
        "coverage_improvement_pct": coverage_improvement,
        "gaps_addressed": sorted(list(gaps_addressed_set)),
        "tasks": tasks,
    }

    # 6. Database persistence
    if persist:
        db_mission = Mission(
            id=mission_id,
            title=mission_record["title"],
            objective=mission_record["objective"],
            target_site_id=site_id,
            volunteer_count=volunteer_count,
            available_time_minutes=available_time_minutes,
            expected_information_gain=normalized_info_gain,
            coverage_improvement_pct=coverage_improvement,
            gaps_addressed=mission_record["gaps_addressed"],
        )
        db.add(db_mission)

        for t in tasks:
            db_task = MissionTask(
                id=t["id"],
                mission_id=mission_id,
                volunteer_index=t["volunteer_index"],
                volunteer_name=t["volunteer_name"],
                target_location_name=t["target_location_name"],
                latitude=t["latitude"],
                longitude=t["longitude"],
                target_observation_type=t["target_observation_type"],
                priority=t["priority"],
                estimated_duration_min=t["estimated_duration_min"],
                expected_gain=t["expected_gain"],
                instructions=t["instructions"],
            )
            db.add(db_task)

        await db.commit()

    return mission_record
