"""HL7 FHIR R4 Export Engine for AQUARYS Environmental Intelligence and Ecological Diagnostics."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aquarys.models import (
    Measurement,
    Observation,
    OracleInvestigation,
    Site,
)

# Standard LOINC codes for aquatic and water quality telemetry
LOINC_PARAMETER_MAP = {
    "dissolved_oxygen": {
        "code": "2710-2",
        "display": "Oxygen [Mass/volume] in Water",
        "ucum": "mg/L",
    },
    "do": {"code": "2710-2", "display": "Oxygen [Mass/volume] in Water", "ucum": "mg/L"},
    "nitrate": {"code": "24376-6", "display": "Nitrate [Mass/volume] in Water", "ucum": "mg/L"},
    "no3": {"code": "24376-6", "display": "Nitrate [Mass/volume] in Water", "ucum": "mg/L"},
    "turbidity": {"code": "24398-0", "display": "Turbidity of Water", "ucum": "[NTU]"},
    "ph": {"code": "2744-1", "display": "pH of Water", "ucum": "[pH]"},
    "water_temperature": {"code": "2712-8", "display": "Temperature of Water", "ucum": "Cel"},
    "temperature": {"code": "2712-8", "display": "Temperature of Water", "ucum": "Cel"},
    "conductivity": {
        "code": "24388-1",
        "display": "Specific conductance of Water",
        "ucum": "uS/cm",
    },
    "phosphate": {"code": "24378-2", "display": "Phosphate [Mass/volume] in Water", "ucum": "mg/L"},
}


async def export_investigation_to_fhir_bundle(
    db: AsyncSession,
    investigation_id: str,
) -> dict[str, Any]:
    """Generate a standard HL7 FHIR R4 Bundle containing DiagnosticReport, Location, and Observation resources."""
    # 1. Fetch Investigation
    inv_stmt = select(OracleInvestigation).where(OracleInvestigation.id == investigation_id)
    inv_res = await db.execute(inv_stmt)
    inv = inv_res.scalar_one_or_none()
    if not inv:
        raise ValueError(f"Investigation {investigation_id} not found")

    site_id = inv.site_id

    # 2. Fetch Site
    site_stmt = select(Site).where(Site.id == site_id)
    site_res = await db.execute(site_stmt)
    site = site_res.scalar_one_or_none()
    if not site:
        raise ValueError(f"Site {site_id} not found")

    # 3. Fetch Measurements & Observations for the site
    meas_stmt = select(Measurement).where(Measurement.site_id == site_id)
    meas_res = await db.execute(meas_stmt)
    measurements = meas_res.scalars().all()

    obs_stmt = (
        select(Observation)
        .options(selectinload(Observation.assessment))
        .where(Observation.site_id == site_id)
    )
    obs_res = await db.execute(obs_stmt)
    observations = obs_res.scalars().all()

    bundle_id = f"bundle-{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(UTC).isoformat()

    entries: list[dict[str, Any]] = []
    result_references: list[dict[str, str]] = []

    # A. Location Resource (Stream Site)
    location_resource = {
        "resourceType": "Location",
        "id": site.id,
        "identifier": [
            {
                "system": "http://aquarys.org/fhir/sid/sites",
                "value": site.id,
            },
            {
                "system": "http://aquarys.org/fhir/sid/site-code",
                "value": site.code or site.id,
            },
        ],
        "status": "active",
        "name": site.name,
        "description": site.description
        or f"Monitoring reach for {site.name} ({site.city}, {site.country})",
        "mode": "instance",
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-EntityCode",
                        "code": "RVR",
                        "display": "River or Stream",
                    }
                ]
            }
        ],
        "address": {
            "city": site.city,
            "country": site.country,
        },
        "position": {
            "latitude": site.latitude,
            "longitude": site.longitude,
            "altitude": site.altitude_m or 0.0,
        },
    }
    entries.append(
        {
            "fullUrl": f"urn:uuid:location-{site.id}",
            "resource": location_resource,
        }
    )

    # B. Measurement Observations
    for m in measurements:
        param_clean = m.parameter.lower().replace(" ", "_") if m.parameter else "unknown"
        loinc_info = LOINC_PARAMETER_MAP.get(
            param_clean,
            {
                "code": "65759-3",
                "display": m.parameter or "Water Quality Measurement",
                "ucum": m.unit or "unit",
            },
        )
        obs_ref_id = f"meas-{m.id}"
        m_obs_resource = {
            "resourceType": "Observation",
            "id": obs_ref_id,
            "identifier": [
                {
                    "system": "http://aquarys.org/fhir/sid/measurements",
                    "value": m.id,
                }
            ],
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "laboratory",
                            "display": "Laboratory / Sensor Telemetry",
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": loinc_info["code"],
                        "display": loinc_info["display"],
                    }
                ],
                "text": m.parameter,
            },
            "subject": {
                "reference": f"Location/{site.id}",
                "display": site.name,
            },
            "effectiveDateTime": m.observed_at.isoformat() if m.observed_at else now_iso,
            "valueQuantity": {
                "value": float(m.value) if m.value is not None else 0.0,
                "unit": m.unit or loinc_info["ucum"],
                "system": "http://unitsofmeasure.org",
                "code": loinc_info["ucum"],
            },
            "extension": [
                {
                    "url": "http://aquarys.org/fhir/StructureDefinition/data-provenance",
                    "valueString": f"Source: {m.source or 'OAH Sensor Network'}",
                }
            ],
        }
        entries.append(
            {
                "fullUrl": f"urn:uuid:{obs_ref_id}",
                "resource": m_obs_resource,
            }
        )
        result_references.append(
            {
                "reference": f"Observation/{obs_ref_id}",
                "display": f"{m.parameter}: {m.value} {m.unit}",
            }
        )

    # C. Qualitative Citizen Observations
    for o in observations:
        obs_ref_id = f"obs-{o.id}"
        components = []
        if o.water_clarity:
            components.append(
                {
                    "code": {"text": "Water Clarity"},
                    "valueString": o.water_clarity,
                }
            )
        if o.odor:
            components.append(
                {
                    "code": {"text": "Odor"},
                    "valueString": o.odor,
                }
            )
        if o.flow_rate_category:
            components.append(
                {
                    "code": {"text": "Flow Rate Category"},
                    "valueString": o.flow_rate_category,
                }
            )
        if o.algae_coverage_pct is not None:
            components.append(
                {
                    "code": {"text": "Algae Coverage Percentage"},
                    "valueQuantity": {"value": o.algae_coverage_pct, "unit": "%"},
                }
            )
        if o.canopy_cover_pct is not None:
            components.append(
                {
                    "code": {"text": "Riparian Canopy Cover Percentage"},
                    "valueQuantity": {"value": o.canopy_cover_pct, "unit": "%"},
                }
            )

        confidence_val = o.assessment.overall_confidence if o.assessment else 0.85

        c_obs_resource = {
            "resourceType": "Observation",
            "id": obs_ref_id,
            "identifier": [
                {
                    "system": "http://aquarys.org/fhir/sid/observations",
                    "value": o.id,
                }
            ],
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "survey",
                            "display": "Citizen Science Field Survey",
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://aquarys.org/fhir/codes/observation",
                        "code": "citizen-stream-survey",
                        "display": "Citizen Stream Visual and Sensory Survey",
                    }
                ],
                "text": "Citizen Ecological Stream Observation",
            },
            "subject": {
                "reference": f"Location/{site.id}",
                "display": site.name,
            },
            "effectiveDateTime": o.observed_at.isoformat() if o.observed_at else now_iso,
            "component": components,
            "extension": [
                {
                    "url": "http://aquarys.org/fhir/StructureDefinition/trust-confidence",
                    "valueDecimal": float(round(confidence_val, 3)),
                },
                {
                    "url": "http://aquarys.org/fhir/StructureDefinition/observer-type",
                    "valueString": o.observer_type or "citizen",
                },
            ],
        }
        entries.append(
            {
                "fullUrl": f"urn:uuid:{obs_ref_id}",
                "resource": c_obs_resource,
            }
        )
        result_references.append(
            {
                "reference": f"Observation/{obs_ref_id}",
                "display": f"Observation {o.id} ({o.water_clarity or 'Survey'})",
            }
        )

    # D. RiskAssessment / Epistemic Hypotheses
    for idx, h in enumerate(inv.hypotheses or []):
        hypo_id = f"risk-hypothesis-{idx + 1}-{inv.id[:8]}"
        hypo_statement = h.get("statement", "")
        plausibility = float(h.get("plausibility_score", 0.7))
        risk_resource = {
            "resourceType": "RiskAssessment",
            "id": hypo_id,
            "status": "final",
            "subject": {
                "reference": f"Location/{site.id}",
                "display": site.name,
            },
            "occurrenceDateTime": inv.created_at.isoformat() if inv.created_at else now_iso,
            "summary": hypo_statement,
            "prediction": [
                {
                    "outcome": {
                        "text": hypo_statement,
                    },
                    "probabilityDecimal": round(plausibility, 3),
                    "rationale": h.get("remaining_uncertainty")
                    or "Evaluated via Grounded Oracle & Multi-Source Triangulation.",
                }
            ],
            "mitigation": h.get("skeptic_challenge")
            or "Verify against counter-evidence and upcoming volunteer sampling.",
        }
        entries.append(
            {
                "fullUrl": f"urn:uuid:{hypo_id}",
                "resource": risk_resource,
            }
        )

    # E. Main DiagnosticReport Resource
    report_resource = {
        "resourceType": "DiagnosticReport",
        "id": f"report-{inv.id}",
        "identifier": [
            {
                "system": "http://aquarys.org/fhir/sid/investigations",
                "value": inv.id,
            }
        ],
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                        "code": "ENV",
                        "display": "Environmental Health Assessment",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://aquarys.org/fhir/codes/reports",
                    "code": "ecological-oracle-investigation",
                    "display": "AQUARYS Ecological Oracle Investigation & Diagnostic Report",
                }
            ],
            "text": inv.question,
        },
        "subject": {
            "reference": f"Location/{site.id}",
            "display": site.name,
        },
        "effectiveDateTime": inv.created_at.isoformat() if inv.created_at else now_iso,
        "issued": now_iso,
        "result": result_references,
        "conclusion": inv.finding,
        "extension": [
            {
                "url": "http://aquarys.org/fhir/StructureDefinition/provider-used",
                "valueString": inv.provider_used or "demo",
            },
            {
                "url": "http://aquarys.org/fhir/StructureDefinition/counter-evidence",
                "valueString": "; ".join(inv.counter_evidence or []),
            },
            {
                "url": "http://aquarys.org/fhir/StructureDefinition/data-gaps",
                "valueString": "; ".join([g.get("gap", str(g)) for g in (inv.data_gaps or [])]),
            },
            {
                "url": "http://aquarys.org/fhir/StructureDefinition/caveats",
                "valueString": "; ".join(inv.caveats or []),
            },
        ],
    }

    # Put DiagnosticReport as first entry in the Bundle
    entries.insert(
        0,
        {
            "fullUrl": f"urn:uuid:report-{inv.id}",
            "resource": report_resource,
        },
    )

    # Assemble FHIR Bundle
    fhir_bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {
            "lastUpdated": now_iso,
            "profile": [
                "http://aquarys.org/fhir/StructureDefinition/environmental-diagnostic-bundle"
            ],
        },
        "type": "document",
        "timestamp": now_iso,
        "total": len(entries),
        "entry": entries,
    }

    return fhir_bundle
