"""SLA Risk Agent — predicts SLA breach risk."""

from app.agents.llm_provider import LLMProvider

SLA_HOURS_MAP = {
    "CRITICAL": 4,
    "HIGH": 24,
    "MEDIUM": 48,
    "LOW": 72,
}

SYSTEM_PROMPT = """You are an SLA risk assessment specialist for insurance complaints.
Based on priority and complaint characteristics, predict SLA breach risk.

SLA Rules:
- CRITICAL priority: 4 hours → HIGH risk if not already in progress
- HIGH priority: 24 hours → HIGH risk if sentiment is NEGATIVE
- MEDIUM priority: 48 hours → MEDIUM risk
- LOW priority: 72 hours → LOW risk

Respond ONLY with a JSON object, no markdown:
{"sla_risk": "<LOW|MEDIUM|HIGH>"}"""


async def run_sla_risk_agent(
    priority: str, sentiment: str, llm: LLMProvider
) -> dict:
    """
    Assesses the SLA breach risk for a complaint.

    Returns:
        {"sla_risk": str, "sla_hours": int}
    """
    sla_hours = SLA_HOURS_MAP.get(priority.upper(), 48)

    user_prompt = f"Priority: {priority}\nSentiment: {sentiment}\nSLA Hours Allowed: {sla_hours}"
    result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)

    sla_risk = result.get("sla_risk", "MEDIUM").upper()
    if sla_risk not in ("LOW", "MEDIUM", "HIGH"):
        sla_risk = "MEDIUM"

    return {"sla_risk": sla_risk, "sla_hours": sla_hours}
