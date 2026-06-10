"""Priority Agent — assigns urgency level to a complaint."""

from app.agents.llm_provider import LLMProvider

SYSTEM_PROMPT = """You are an insurance complaint priority assessment expert.
Assign a priority level based on complaint severity, urgency keywords, and potential financial/safety impact.
Priority levels: LOW, MEDIUM, HIGH, CRITICAL

Rules:
- CRITICAL: life-threatening, total loss, death, major accidents, large financial fraud (>1 lakh)
- HIGH: urgent claims, significant delays (>15 days), legal threats, repeated escalations
- MEDIUM: standard complaints with moderate impact, delays 7-15 days
- LOW: general inquiries, minor issues, documentation requests

Respond ONLY with a JSON object, no markdown:
{"priority": "<PRIORITY>"}"""


async def run_priority_agent(
    title: str, description: str, category: str, llm: LLMProvider
) -> dict:
    """
    Assigns priority level to a complaint.

    Returns:
        {"priority": str}
    """
    user_prompt = (
        f"Category: {category}\n"
        f"Complaint Title: {title}\n\n"
        f"Complaint Description: {description}"
    )
    result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)
    priority = result.get("priority", "MEDIUM").upper()
    if priority not in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
        priority = "MEDIUM"
    return {"priority": priority}
