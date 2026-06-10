"""
LLM Provider Abstraction Layer

This abstraction allows easy swapping between:
- MockProvider (used for development/demo/testing)
- QwenProvider (AMD GPU - future)
- LlamaProvider (AMD GPU - future)
- DeepSeekProvider (AMD GPU - future)

To add a new provider: subclass LLMProvider and implement `complete()`.
"""

from __future__ import annotations
import abc
import json
import re
import random
from app.core.config import settings


class LLMProvider(abc.ABC):
    """Abstract base class for all LLM providers."""

    @abc.abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt to the LLM and return the text response.

        Args:
            system_prompt: Instructions for how the model should behave.
            user_prompt: The actual input/question.

        Returns:
            Raw string response from the LLM.
        """
        ...

    async def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Convenience method: calls complete() and parses the JSON response.
        Strips markdown code fences if present.
        """
        raw = await self.complete(system_prompt, user_prompt)
        # Strip markdown json fences if model wraps response
        cleaned = re.sub(r"```json\s*|\s*```", "", raw).strip()
        return json.loads(cleaned)


# ---------------------------------------------------------------------------
# Mock Provider — deterministic, keyword-based, zero-latency
# ---------------------------------------------------------------------------

CLAIMS_KEYWORDS = ["claim", "claims", "accident", "damage", "repair", "hospital", "surgery",
                   "treatment", "reimbursement", "cashless", "pending claim", "settlement"]
SURVEYOR_KEYWORDS = ["surveyor", "survey", "assessment", "inspection", "property", "valuation",
                     "site visit", "assessor"]
BILLING_KEYWORDS = ["premium", "billing", "payment", "refund", "overcharged", "invoice",
                    "deduction", "emi", "auto-debit", "receipt", "amount deducted"]
FRAUD_KEYWORDS = ["fraud", "scam", "fake", "forged", "cheating", "stolen", "impersonation",
                  "misrepresentation", "unauthorized", "suspicious"]
POLICY_KEYWORDS = ["policy", "renewal", "cancel", "endorsement", "document", "certificate",
                   "coverage", "exclusion", "terms", "nominee", "maturity"]

HIGH_URGENCY_KEYWORDS = ["urgent", "immediately", "asap", "critical", "emergency",
                         "serious", "dangerous", "life-threatening", "hospitalised", "hospitalized"]
CRITICAL_KEYWORDS = ["death", "deceased", "fatal", "life", "catastrophic", "total loss", "fire",
                     "flood", "accident", "icu", "intensive care"]
NEGATIVE_KEYWORDS = ["angry", "frustrated", "terrible", "worst", "horrible", "disappointed",
                     "unacceptable", "pathetic", "useless", "disgusted", "fed up", "escalate",
                     "legal", "consumer court", "lawsuit"]
POSITIVE_KEYWORDS = ["thank", "good", "great", "excellent", "happy", "satisfied",
                     "resolved", "appreciate", "helpful"]


class MockProvider(LLMProvider):
    """
    A fully deterministic mock LLM provider.
    Uses keyword analysis for realistic classifications — no API calls needed.
    Perfect for demos, CI, and local development.
    """

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        # Parse task type from system prompt
        task = system_prompt.lower()
        text = user_prompt.lower()

        if "classify" in task and "category" in task:
            return self._classify(text)
        elif "priority" in task:
            return self._prioritize(text)
        elif "route" in task or "routing" in task:
            return self._route(text)
        elif "sentiment" in task:
            return self._sentiment(text)
        elif "sla" in task or "risk" in task:
            return self._sla_risk(text)
        elif "supervisor" in task or "summary" in task:
            return self._supervisor(text)
        else:
            return json.dumps({"result": "ok"})

    def _classify(self, text: str) -> str:
        scores = {
            "CLAIMS": sum(1 for kw in CLAIMS_KEYWORDS if kw in text),
            "SURVEYOR": sum(1 for kw in SURVEYOR_KEYWORDS if kw in text),
            "BILLING": sum(1 for kw in BILLING_KEYWORDS if kw in text),
            "FRAUD": sum(1 for kw in FRAUD_KEYWORDS if kw in text),
            "POLICY_ADMIN": sum(1 for kw in POLICY_KEYWORDS if kw in text),
        }
        best = max(scores, key=scores.get)
        best_score = scores[best]
        if best_score == 0:
            best = "OTHER"
            confidence = round(random.uniform(0.55, 0.70), 2)
        else:
            confidence = min(0.95, round(0.65 + (best_score * 0.08) + random.uniform(0, 0.05), 2))
        return json.dumps({"category": best, "confidence": confidence})

    def _prioritize(self, text: str) -> str:
        if any(kw in text for kw in CRITICAL_KEYWORDS):
            priority = "CRITICAL"
        elif any(kw in text for kw in HIGH_URGENCY_KEYWORDS):
            priority = "HIGH"
        elif any(kw in text for kw in NEGATIVE_KEYWORDS):
            priority = "HIGH"
        elif len(text) > 400:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        return json.dumps({"priority": priority})

    def _route(self, text: str) -> str:
        category_map = {
            "CLAIMS": "Claims Operations Team",
            "SURVEYOR": "Property Assessment Team",
            "POLICY_ADMIN": "Policy Administration Team",
            "BILLING": "Billing & Premium Team",
            "FRAUD": "Special Investigation Unit",
            "OTHER": "Claims Operations Team",
        }
        # Try to find category hint in the text
        for cat, team in category_map.items():
            if cat.lower() in text:
                return json.dumps({"assigned_team": team, "team_type": cat})
        return json.dumps({"assigned_team": "Claims Operations Team", "team_type": "CLAIMS"})

    def _sentiment(self, text: str) -> str:
        neg_score = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text)
        pos_score = sum(1 for kw in POSITIVE_KEYWORDS if kw in text)
        if neg_score > pos_score:
            sentiment = "NEGATIVE"
        elif pos_score > neg_score:
            sentiment = "POSITIVE"
        else:
            sentiment = "NEUTRAL"
        return json.dumps({"sentiment": sentiment})

    def _sla_risk(self, text: str) -> str:
        if "critical" in text or "4 hour" in text:
            risk = "HIGH"
        elif "high" in text or "24 hour" in text:
            risk = "HIGH"
        elif "medium" in text or "48 hour" in text:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        return json.dumps({"sla_risk": risk})

    def _supervisor(self, text: str) -> str:
        # Extract structured data from combined analysis text
        lines = text.lower()
        reason = "Complaint analyzed and classified based on content and severity indicators."
        suggested = "Review complaint details and take appropriate action within SLA timeline."
        return json.dumps({"reason": reason, "suggested_action": suggested})


# ---------------------------------------------------------------------------
# Future AMD GPU Providers (stub implementations)
# ---------------------------------------------------------------------------

class QwenProvider(LLMProvider):
    """
    Future provider: Qwen model hosted on AMD GPU (ROCm).
    Set LLM_PROVIDER=qwen and AMD_API_URL in .env.
    """

    def __init__(self, base_url: str, model: str = "qwen2.5-72b-instruct"):
        self.base_url = base_url
        self.model = model

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.1,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]


class LlamaProvider(LLMProvider):
    """
    Future provider: Llama 3.x model hosted on AMD GPU (ROCm).
    Compatible with OpenAI-style API endpoints (vLLM / Ollama).
    """

    def __init__(self, base_url: str, model: str = "llama-3.1-70b-instruct"):
        self.base_url = base_url
        self.model = model

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.1,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]


class DeepSeekProvider(LLMProvider):
    """
    Future provider: DeepSeek model on AMD GPU or DeepSeek API.
    """

    def __init__(self, base_url: str, api_key: str = "", model: str = "deepseek-chat"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        import httpx
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.1,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Provider Factory
# ---------------------------------------------------------------------------

def get_llm_provider() -> LLMProvider:
    """
    Factory function: returns the correct LLMProvider based on LLM_PROVIDER env var.
    Swap providers without touching agent logic.
    """
    provider = settings.LLM_PROVIDER.lower()
    if provider == "mock":
        return MockProvider()
    elif provider == "qwen":
        import os
        return QwenProvider(base_url=os.environ.get("AMD_API_URL", "http://localhost:8080"))
    elif provider == "llama":
        import os
        return LlamaProvider(base_url=os.environ.get("AMD_API_URL", "http://localhost:8080"))
    elif provider == "deepseek":
        import os
        return DeepSeekProvider(
            base_url=os.environ.get("AMD_API_URL", "https://api.deepseek.com"),
            api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Valid: mock, qwen, llama, deepseek")
