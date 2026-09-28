"""API router for Evidence Export & FHIR Document operations."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.services.fhir.exporter import export_investigation_to_fhir_bundle

router = APIRouter(prefix="/exports", tags=["Evidence Export (FHIR)"])


@router.get("/fhir/{investigation_id}", response_model=dict[str, Any])
async def export_investigation_fhir(
    investigation_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Export a grounded Oracle Investigation and supporting evidence to an HL7 FHIR R4 Bundle.

    The resulting Document Bundle contains:
    - DiagnosticReport (investigation findings, research questions)
    - Location (stream monitoring site geospatial coordinates)
    - Observation (chemical/sensor measurements mapped to LOINC standard)
    - Observation (citizen qualitative surveys mapped to Aquarys terminology)
    - RiskAssessment (epistemic hypotheses, plausibility, skeptic challenges)
    """
    try:
        fhir_bundle = await export_investigation_to_fhir_bundle(db, investigation_id)
        return fhir_bundle
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
