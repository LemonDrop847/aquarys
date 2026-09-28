"""Deterministic Demo LLM Provider for 100% offline uptime and reproducible benchmarks."""

import uuid
from typing import Any

from aquarys.services.oracle.providers.base import (
    ChallengeResult,
    HypothesisResult,
    InvestigationSynthesis,
    LLMProvider,
)


class DemoProvider(LLMProvider):
    """Deterministic provider evaluating real evidence graph & telemetry data."""

    async def synthesize_investigation(
        self,
        site_context: dict[str, Any],
        evidence_graph: dict[str, Any],
        twin_context: list[dict[str, Any]],
        question: str,
    ) -> InvestigationSynthesis:
        site_name = site_context.get("name", "Target Stream")
        site_id = site_context.get("id", "SITE-01")
        wq_score = site_context.get("water_quality_score", 50.0) or 50.0
        veg_score = site_context.get("vegetation_score", 50.0) or 50.0
        contradictions = evidence_graph.get("contradictions", [])
        supports = evidence_graph.get("supports", [])

        # Grounded fact generation
        facts = [
            f"Site {site_name} ({site_id}) ecological health index: Water Quality={wq_score:.1f}/100, Vegetation={veg_score:.1f}/100.",
            f"Relational Evidence Graph constructed with {evidence_graph.get('node_count', 0)} nodes and {evidence_graph.get('edge_count', 0)} edges.",
        ]
        if contradictions:
            facts.append(f"Detected {len(contradictions)} conflicting signal(s) between visual citizen reports and analytical sensor data.")
        if supports:
            facts.append(f"Corroborated {len(supports)} multi-modal observation and satellite telemetry links.")

        # Grounded Hypotheses
        hypotheses = []
        if wq_score < 50.0:
            h1 = HypothesisResult(
                id=f"hyp_{uuid.uuid4().hex[:6]}",
                statement="Chronic organic and nutrient loading is driving hypoxic stream conditions and benthic degradation.",
                plausibility_score=0.88,
                supporting_evidence_ids=[e["edge_id"] for e in supports[:3]],
                counter_evidence="Occasional clear water visual observations during high-flow dilution events.",
                skeptic_challenge="Nutrient surges may be episodic storm runoff rather than continuous point-source discharge.",
                remaining_uncertainty="Diurnal dissolved oxygen minimums during pre-dawn hours are unmeasured.",
            )
            hypotheses.append(h1)
        else:
            h1 = HypothesisResult(
                id=f"hyp_{uuid.uuid4().hex[:6]}",
                statement="Riparian corridor buffering maintains stable baseflow water quality despite urban catchment pressure.",
                plausibility_score=0.85,
                supporting_evidence_ids=[e["edge_id"] for e in supports[:3]],
                counter_evidence="Localized micro-litter accumulation noted at footbridge access points.",
                skeptic_challenge="High canopy cover may obscure localized algal blooms in shallow backwaters.",
                remaining_uncertainty="Nutrient dynamics during summer baseflow recession need higher temporal frequency.",
            )
            hypotheses.append(h1)

        # Counter Evidence
        counter_evidence = [
            c.get("reason", "Discrepancy in multi-sensor reading") for c in contradictions
        ]
        if not counter_evidence:
            counter_evidence = [
                "No direct chemical sensor contradiction found; however, citizen sampling exhibits high weekend-only temporal bias."
            ]

        # Knowledge Gaps
        data_gaps = []
        dim_status = site_context.get("dimension_status", {})
        for dim, status in dim_status.items():
            if status in ["missing", "estimated"]:
                data_gaps.append({
                    "dimension": dim,
                    "status": status,
                    "severity": "HIGH" if status == "missing" else "MEDIUM",
                    "recommendation": f"Deploy targeted citizen mission to sample ground truth for {dim.replace('_', ' ')}.",
                })

        if not data_gaps:
            data_gaps.append({
                "dimension": "macroinvertebrates",
                "status": "missing",
                "severity": "MEDIUM",
                "recommendation": "Perform biological BMWP / ASPT kick-sampling to confirm long-term ecological integrity.",
            })

        # Next Observations
        next_observations = [
            {
                "priority": "HIGH",
                "target": "Dissolved Oxygen Pre-Dawn Logging",
                "action": "Deploy continuous optical DO logger for 48 hours to capture respiration dips.",
            },
            {
                "priority": "MEDIUM",
                "target": "Riparian Structure Verification",
                "action": "Photo-document canopy continuity and bank erosion 100m upstream and downstream.",
            },
        ]

        # Caveats
        caveats = [
            "Epistemic confidence capped by temporal sparsity of citizen observations.",
            "Satellite EO indices (NDVI/NDWI) have 10m spatial resolution and average in-stream channels with riparian margins.",
        ]

        # Primary Finding
        finding = (
            f"Evidence synthesis for {site_name} indicates {'substantially degraded' if wq_score < 50 else 'resilient and healthy'} "
            f"stream condition (Overall Water Quality: {wq_score:.1f}/100). "
            f"Identified {len(hypotheses)} primary causal hypothesis, corroborated by {len(supports)} relational links "
            f"and challenged by {len(contradictions)} telemetry anomalies."
        )

        evidence_ids = [e.get("edge_id", f"edge_{i}") for i, e in enumerate(supports + contradictions)]

        return InvestigationSynthesis(
            finding=finding,
            facts=facts,
            hypotheses=hypotheses,
            counter_evidence=counter_evidence,
            data_gaps=data_gaps,
            next_observations=next_observations,
            caveats=caveats,
            evidence_ids=evidence_ids,
        )

    async def challenge_hypothesis(
        self,
        hypothesis_statement: str,
        supporting_evidence: list[dict[str, Any]],
        site_context: dict[str, Any],
    ) -> ChallengeResult:
        return ChallengeResult(
            hypothesis_id=f"hyp_{uuid.uuid4().hex[:6]}",
            original_plausibility=0.85,
            adjusted_plausibility=0.68,
            skeptic_critique="Hypothesis assumes continuous discharge but neglects potential episodic dilution and stormwater bypass effects.",
            identified_counter_evidence=[
                "Turbidity spikes correlate with precipitation events rather than continuous baseline flow.",
                "Citizen visual observations report clear water periods between rain events.",
            ],
            epistemic_weaknesses=[
                "Sparse temporal coverage (samples collected primarily on weekends).",
                "Absence of upstream biological indicator data (BMWP score).",
            ],
            suggested_verification_test="Conduct high-frequency 15-minute electrical conductivity and turbidity logging across a complete rain event cycle.",
        )
