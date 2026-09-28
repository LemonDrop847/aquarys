"""Google Gemini LLM provider for grounded Oracle synthesis."""

import json
from typing import Any

from aquarys.core.config import settings
from aquarys.services.oracle.providers.base import (
    ChallengeResult,
    HypothesisResult,
    InvestigationSynthesis,
    LLMProvider,
)
from aquarys.services.oracle.providers.demo import DemoProvider


class GeminiProvider(LLMProvider):
    """Google Gemini provider with graceful fallback to DemoProvider if unconfigured."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-pro") -> None:
        self.api_key = api_key or settings.gemini_api_key
        self.model = model
        self.fallback = DemoProvider()

    async def synthesize_investigation(
        self,
        site_context: dict[str, Any],
        evidence_graph: dict[str, Any],
        twin_context: list[dict[str, Any]],
        question: str,
    ) -> InvestigationSynthesis:
        if not self.api_key:
            return await self.fallback.synthesize_investigation(
                site_context, evidence_graph, twin_context, question
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                self.model,
                generation_config={"response_mime_type": "application/json"},
            )

            prompt = f"""
            You are the AQUARYS Environmental Intelligence Oracle. Synthesize stream telemetry into an epistemic investigation.
            Question: {question}
            Site Context: {json.dumps(site_context)}
            Evidence Graph: {json.dumps(evidence_graph)}
            Ecological Twins: {json.dumps(twin_context)}

            Return JSON matching the schema:
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
            resp = await model.generate_content_async(prompt)
            data = json.loads(resp.text)
            return InvestigationSynthesis(**data)
        except Exception:
            return await self.fallback.synthesize_investigation(
                site_context, evidence_graph, twin_context, question
            )

    async def challenge_hypothesis(
        self,
        hypothesis_statement: str,
        supporting_evidence: list[dict[str, Any]],
        site_context: dict[str, Any],
    ) -> ChallengeResult:
        if not self.api_key:
            return await self.fallback.challenge_hypothesis(
                hypothesis_statement, supporting_evidence, site_context
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                self.model,
                generation_config={"response_mime_type": "application/json"},
            )
            prompt = f"""
            Act as an adversarial scientific skeptic reviewing this aquatic ecological hypothesis:
            Hypothesis: "{hypothesis_statement}"
            Supporting Evidence: {json.dumps(supporting_evidence)}
            Site Context: {json.dumps(site_context)}

            Return JSON:
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
            resp = await model.generate_content_async(prompt)
            data = json.loads(resp.text)
            return ChallengeResult(**data)
        except Exception:
            return await self.fallback.challenge_hypothesis(
                hypothesis_statement, supporting_evidence, site_context
            )
