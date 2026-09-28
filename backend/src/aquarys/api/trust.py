"""FastAPI router for Trust Engine and Evidence Evaluation."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.models import EOMeasurement, EvidenceAssessment, Measurement, Observation, Site
from aquarys.schemas.trust import EvidenceAssessmentResponse, TrustEvaluateRequest
from aquarys.services.trust.evaluator import evaluate_observation_trust

router = APIRouter(tags=["Trust Engine"])


@router.post(
    "/trust/evaluate",
    response_model=EvidenceAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate trust and evidence quality for an observation",
)
async def evaluate_trust_endpoint(
    payload: TrustEvaluateRequest,
    db: AsyncSession = Depends(get_db),
) -> EvidenceAssessmentResponse:
    """Evaluates multi-dimensional evidence strength and returns an evidence profile."""
    obs_id = payload.observation_id
    obs_dict = payload.observation_data or {}
    site_dict = None

    if obs_id:
        result = await db.execute(select(Observation).where(Observation.id == obs_id))
        obs_record = result.scalar_one_or_none()
        if not obs_record:
            raise HTTPException(status_code=404, detail=f"Observation with id '{obs_id}' not found")

        obs_dict = {
            "id": obs_record.id,
            "site_id": obs_record.site_id,
            "observed_at": obs_record.observed_at,
            "observer_id": obs_record.observer_id,
            "latitude": obs_record.latitude,
            "longitude": obs_record.longitude,
            "water_clarity": obs_record.water_clarity,
            "flow_rate_category": obs_record.flow_rate_category,
            "odor": obs_record.odor,
            "algae_coverage_pct": obs_record.algae_coverage_pct,
            "litter_present": obs_record.litter_present,
            "canopy_cover_pct": obs_record.canopy_cover_pct,
            "image_urls": obs_record.image_urls,
            "notes": obs_record.notes,
            "raw_payload_hash": obs_record.raw_payload_hash,
        }

        # Fetch site context
        site_res = await db.execute(select(Site).where(Site.id == obs_record.site_id))
        site_record = site_res.scalar_one_or_none()
        if site_record:
            site_dict = {
                "latitude": site_record.latitude,
                "longitude": site_record.longitude,
                "name": site_record.name,
            }

    if not obs_dict:
        raise HTTPException(
            status_code=400,
            detail="Must provide either valid observation_id or observation_data in request",
        )

    # Fetch context: existing observations, measurements, eo_data
    site_id = obs_dict.get("site_id")
    existing_obs = []
    measurements = []
    eo_data = []

    if site_id:
        obs_query = await db.execute(
            select(Observation).where(Observation.site_id == site_id).limit(50)
        )
        for o in obs_query.scalars().all():
            existing_obs.append(
                {
                    "id": o.id,
                    "observer_id": o.observer_id,
                    "observed_at": o.observed_at,
                    "latitude": o.latitude,
                    "longitude": o.longitude,
                    "water_clarity": o.water_clarity,
                    "raw_payload_hash": o.raw_payload_hash,
                }
            )

        meas_query = await db.execute(
            select(Measurement).where(Measurement.site_id == site_id).limit(50)
        )
        for m in meas_query.scalars().all():
            measurements.append(
                {
                    "parameter_name": m.parameter,
                    "value": m.value,
                    "unit": m.unit,
                }
            )

        eo_query = await db.execute(
            select(EOMeasurement).where(EOMeasurement.site_id == site_id).limit(20)
        )
        for eo in eo_query.scalars().all():
            eo_data.append(
                {
                    "ndwi": eo.ndwi,
                    "ndvi": eo.ndvi,
                }
            )

    profile = evaluate_observation_trust(
        observation_data=obs_dict,
        site_data=site_dict,
        existing_observations=existing_obs,
        measurements=measurements,
        eo_data=eo_data,
    )

    assessment_id = f"ea-{obs_id or uuid.uuid4().hex[:12]}"
    reasoning_summary = (
        f"Confidence {profile.overall_confidence:.2f} based on completeness ({profile.completeness:.2f}), "
        f"consistency ({profile.consistency:.2f}), location ({profile.location:.2f}), and independent evidence."
    )

    assessment_resp = EvidenceAssessmentResponse(
        id=assessment_id,
        observation_id=obs_id or "adhoc",
        evaluated_at=datetime.now(UTC),
        completeness=profile.completeness,
        consistency=profile.consistency,
        location_validity=profile.location,
        temporal_validity=profile.temporal_validity,
        image_support=profile.image_support,
        cross_observer=profile.cross_observer,
        independent_support=profile.independent_support,
        duplicate_risk=profile.duplicate_risk,
        overall_confidence=profile.overall_confidence,
        flags=profile.flags,
        positive_signals=profile.positive_signals,
        negative_signals=profile.negative_signals,
        reasoning=reasoning_summary,
        processing_version="1.0.0",
    )

    if payload.persist and obs_id:
        existing_assess_res = await db.execute(
            select(EvidenceAssessment).where(EvidenceAssessment.observation_id == obs_id)
        )
        existing_assess = existing_assess_res.scalar_one_or_none()

        if existing_assess:
            existing_assess.completeness = profile.completeness
            existing_assess.consistency = profile.consistency
            existing_assess.location_validity = profile.location
            existing_assess.temporal_validity = profile.temporal_validity
            existing_assess.image_support = profile.image_support
            existing_assess.cross_observer = profile.cross_observer
            existing_assess.independent_support = profile.independent_support
            existing_assess.duplicate_risk = profile.duplicate_risk
            existing_assess.overall_confidence = profile.overall_confidence
            existing_assess.flags = profile.flags
            existing_assess.positive_signals = profile.positive_signals
            existing_assess.negative_signals = profile.negative_signals
            existing_assess.reasoning = reasoning_summary
            existing_assess.evaluated_at = datetime.now(UTC)
            assessment_resp.id = existing_assess.id
        else:
            db_assessment = EvidenceAssessment(
                id=assessment_id,
                observation_id=obs_id,
                evaluated_at=datetime.now(UTC),
                completeness=profile.completeness,
                consistency=profile.consistency,
                location_validity=profile.location,
                temporal_validity=profile.temporal_validity,
                image_support=profile.image_support,
                cross_observer=profile.cross_observer,
                independent_support=profile.independent_support,
                duplicate_risk=profile.duplicate_risk,
                overall_confidence=profile.overall_confidence,
                flags=profile.flags,
                positive_signals=profile.positive_signals,
                negative_signals=profile.negative_signals,
                reasoning=reasoning_summary,
                processing_version="1.0.0",
            )
            db.add(db_assessment)

        await db.commit()

    return assessment_resp


@router.get(
    "/observations/{observation_id}/evidence",
    response_model=EvidenceAssessmentResponse,
    summary="Get or evaluate evidence passport for an observation",
)
async def get_observation_evidence(
    observation_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvidenceAssessmentResponse:
    """Retrieves persisted evidence assessment or evaluates on-the-fly."""
    result = await db.execute(
        select(EvidenceAssessment).where(EvidenceAssessment.observation_id == observation_id)
    )
    assessment = result.scalar_one_or_none()
    if assessment:
        return EvidenceAssessmentResponse.model_validate(assessment)

    # Evaluate and persist on-the-fly
    return await evaluate_trust_endpoint(
        payload=TrustEvaluateRequest(observation_id=observation_id, persist=True),
        db=db,
    )
