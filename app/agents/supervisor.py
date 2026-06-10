"""Supervisor Agent — synthesizes all agent outputs into final analysis."""

from app.agents.llm_provider import LLMProvider

REASON_TEMPLATES = {
    ("CLAIMS", "CRITICAL"): "Critical claims complaint requiring immediate attention. High financial or personal impact detected.",
    ("CLAIMS", "HIGH"): "Claims complaint with significant urgency. Customer reports substantial delays or significant loss.",
    ("CLAIMS", "MEDIUM"): "Standard claims processing complaint. Moderate impact requiring timely resolution.",
    ("CLAIMS", "LOW"): "Routine claims inquiry. Informational request or minor administrative issue.",
    ("FRAUD", "CRITICAL"): "Suspected fraudulent activity reported. Requires immediate investigation by Special Investigation Unit.",
    ("FRAUD", "HIGH"): "Potential fraud indicators detected. Priority investigation required.",
    ("BILLING", "HIGH"): "Significant billing discrepancy reported. Customer reports incorrect premium deduction or overcharge.",
    ("BILLING", "MEDIUM"): "Billing query requiring clarification. Premium or payment-related concern.",
    ("SURVEYOR", "HIGH"): "Property assessment complaint with urgency. Customer reports inadequate survey or delayed assessment.",
    ("POLICY_ADMIN", "MEDIUM"): "Policy documentation or administration issue. Requires policy team review.",
}

ACTION_TEMPLATES = {
    ("CLAIMS", "CRITICAL"): "Immediately escalate to senior claims manager. Contact customer within 1 hour. Review and fast-track settlement.",
    ("CLAIMS", "HIGH"): "Assign to senior claims officer. Review claim status within 4 hours and provide customer update.",
    ("CLAIMS", "MEDIUM"): "Assign to claims processing team. Provide status update to customer within 24 hours.",
    ("CLAIMS", "LOW"): "Route to claims support team. Resolve within standard SLA timeline.",
    ("FRAUD", "CRITICAL"): "Immediately freeze related policy. Escalate to SIU head. Do not contact customer until investigation initiated.",
    ("FRAUD", "HIGH"): "Assign to SIU investigator. Gather documentation and initiate investigation protocol.",
    ("BILLING", "HIGH"): "Review billing records immediately. Issue refund or correction within 24 hours if overcharge confirmed.",
    ("BILLING", "MEDIUM"): "Review account statement. Provide detailed billing explanation to customer.",
    ("SURVEYOR", "HIGH"): "Re-assign surveyor or escalate to regional assessment head. Schedule re-survey within 48 hours.",
    ("POLICY_ADMIN", "MEDIUM"): "Review policy documents and resolve administrative query. Update customer on policy status.",
}

DEFAULT_REASON = "Complaint analyzed based on content keywords, priority indicators, and customer sentiment."
DEFAULT_ACTION = "Review complaint details thoroughly and contact customer with resolution within the specified SLA timeline."

SYSTEM_PROMPT = """You are a senior insurance operations supervisor.
Based on the analysis from all agents, provide:
1. A concise reason for the classification (1-2 sentences, professional tone)
2. A specific suggested action for the operations team (1-2 sentences, actionable)

Respond ONLY with a JSON object, no markdown:
{"reason": "<reason>", "suggested_action": "<action>"}"""


async def run_supervisor_agent(
    title: str,
    description: str,
    category: str,
    priority: str,
    assigned_team: str,
    sentiment: str,
    sla_risk: str,
    confidence: float,
    llm: LLMProvider,
) -> dict:
    """
    Supervisor synthesizes all agent outputs into final actionable analysis.

    Returns:
        {"reason": str, "suggested_action": str}
    """
    # Try template lookup first for speed and reliability
    key = (category.upper(), priority.upper())
    reason = REASON_TEMPLATES.get(key)
    action = ACTION_TEMPLATES.get(key)

    # Add sentiment context to reason if negative
    if reason and sentiment.upper() == "NEGATIVE":
        reason += " Customer sentiment is highly negative, indicating significant dissatisfaction."

    if not reason or not action:
        # Use LLM for less common combinations
        user_prompt = (
            f"Category: {category}\n"
            f"Priority: {priority}\n"
            f"Assigned Team: {assigned_team}\n"
            f"Sentiment: {sentiment}\n"
            f"SLA Risk: {sla_risk}\n"
            f"Confidence: {confidence:.0%}\n"
            f"Complaint Title: {title}\n"
            f"Description (excerpt): {description[:300]}"
        )
        result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)
        reason = reason or result.get("reason", DEFAULT_REASON)
        action = action or result.get("suggested_action", DEFAULT_ACTION)

    return {
        "reason": reason or DEFAULT_REASON,
        "suggested_action": action or DEFAULT_ACTION,
    }
