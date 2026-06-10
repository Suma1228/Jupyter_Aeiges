"""Routing Agent — maps category to the correct operations team."""

from app.agents.llm_provider import LLMProvider

CATEGORY_TO_TEAM = {
    "CLAIMS": ("Claims Operations Team", "CLAIMS"),
    "SURVEYOR": ("Property Assessment Team", "SURVEYOR"),
    "POLICY_ADMIN": ("Policy Administration Team", "POLICY_ADMIN"),
    "BILLING": ("Billing & Premium Team", "BILLING"),
    "FRAUD": ("Special Investigation Unit", "FRAUD"),
    "OTHER": ("Claims Operations Team", "CLAIMS"),
}

SYSTEM_PROMPT = """You are an insurance complaint routing specialist.
Based on the category, route the complaint to the correct team.

Category to Team mapping:
- CLAIMS → Claims Operations Team
- SURVEYOR → Property Assessment Team
- POLICY_ADMIN → Policy Administration Team
- BILLING → Billing & Premium Team
- FRAUD → Special Investigation Unit
- OTHER → Claims Operations Team

Respond ONLY with a JSON object, no markdown:
{"assigned_team": "<team name>", "team_type": "<category>"}"""


async def run_routing_agent(
    category: str, title: str, description: str, llm: LLMProvider
) -> dict:
    """
    Routes complaint to the correct team based on category.

    Returns:
        {"assigned_team": str, "team_type": str}
    """
    # Use deterministic mapping first — reliable for routing
    if category in CATEGORY_TO_TEAM:
        team_name, team_type = CATEGORY_TO_TEAM[category]
        return {"assigned_team": team_name, "team_type": team_type}

    # Fallback to LLM if category is unusual
    user_prompt = f"Category: {category}\nComplaint Title: {title}\nDescription: {description}"
    result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)
    return {
        "assigned_team": result.get("assigned_team", "Claims Operations Team"),
        "team_type": result.get("team_type", "CLAIMS"),
    }
