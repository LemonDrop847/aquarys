"""Ollama local LLM provider for grounded Oracle synthesis."""

import json
from typing import Any

import httpx

from aquarys.core.config import settings
from aquarys.services.oracle.providers.base import (
    ChallengeResult,
    InvestigationSynthesis,
    LLMProvider,
)
from aquarys.services.oracle.providers.demo import DemoProvider


class OllamaProvider(LLMProvider):
    """Local Ollama provider with fallback to DemoProvider."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.fallback = DemoProvider()

    async def synthesize_investigation(
        self,
        site_context: dict[str, Any],
        evidence_graph: dict[str, Any],
        twin_context: list[dict[str, Any]],
        question: str,
    ) -> InvestigationSynthesis:
        prompt = f"""
        You are the AQUARYS Environmental Intelligence Oracle. Synthesize stream telemetry into an epistemic investigation.
        Question: {question}
        Site Context: {json.dumps(site_context)}
        Evidence Graph: {json.dumps(evidence_graph)}
        Ecological Twins: {json.dumps(twin_context)}

        Return ONLY valid JSON matching this schema:
        {{
            "finding": "Primary evidence-grounded finding",
            "facts": ["list of grounded empirical facts"],
            "hypotheses": [
                {{
                    "id": "hyp_1",
                    "statement": "Causal explanation",
                    "plausibility_score": 0.85,
                    "supporting_evidence_ids": ["edge_1"],
                    "counter_evidence": "...",
                    "skeptic_challenge": "...",
                    "remaining_uncertainty": "..."
                }}
            ],
            "counter_evidence": ["contradictory telemetry or observations"],
            "data_gaps": [{{"dimension": "...", "status": "missing", "severity": "HIGH", "recommendation": "..."}}],
            "next_observations": [{{"priority": "HIGH", "target": "...", "action": "..."}}],
            "caveats": ["epistemic caveats"],
            "evidence_ids": ["used_edge_ids"]
        }}
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "format": "json",
                        "stream": False,
                    },
                )
                if res.status_code == 200:
                    payload = res.json()
                    response_text = payload.get("response", "{}")
                    data = json.loads(response_text)
                    return InvestigationSynthesis(**data)
        except Exception:
            pass

        return await self.fallback.synthesize_investigation(
            site_context, evidence_graph, twin_context, question
        )

    async def challenge_hypothesis(
        self,
        hypothesis_statement: str,
        supporting_evidence: list[dict[str, Any]],
        site_context: dict[str, Any],
    ) -> ChallengeResult:
        prompt = f"""
        Act as an adversarial scientific skeptic reviewing this aquatic ecological hypothesis:
        Hypothesis: "{hypothesis_statement}"
        Supporting Evidence: {json.dumps(supporting_evidence)}
        Site Context: {json.dumps(site_context)}

        Return ONLY valid JSON:
        {{
            "hypothesis_id": "hyp_challenge",
            "original_plausibility": 0.85,
            "adjusted_plausibility": 0.65,
            "skeptic_critique": "Rigorous adversarial challenge",
            "identified_counter_evidence": ["list of conflicting observations or gaps"],
            "epistemic_weaknesses": ["biases, unmeasured variables"],
            "suggested_verification_test": "Actionable verification test"
        }}
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "format": "json",
                        "stream": False,
                    },
                )
                if res.status_code == 200:
                    payload = res.json()
                    response_text = payload.get("response", "{}")
                    data = json.loads(response_text)
                    return ChallengeResult(**data)
        except Exception:
            pass

        return await self.fallback.challenge_hypothesis(
            hypothesis_statement, supporting_evidence, site_context
        )
