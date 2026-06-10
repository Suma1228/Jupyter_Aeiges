"""Classification Agent — assigns complaint category."""

from app.agents.llm_provider import LLMProvider

SYSTEM_PROMPT = """You are an insurance complaint classification expert.
Classify the complaint into exactly one of these categories:
CLAIMS, SURVEYOR, POLICY_ADMIN, BILLING, FRAUD, OTHER

Respond ONLY with a JSON object, no markdown, no explanation:
{"category": "<CATEGORY>", "confidence": <0.0-1.0>}"""


async def run_classification_agent(
    title: str, description: str, llm: LLMProvider
) -> dict:
    """
    Classifies a complaint into a category with a confidence score.

    Returns:
        {"category": str, "confidence": float}
    """
    user_prompt = f"Complaint Title: {title}\n\nComplaint Description: {description}"
    result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)
    return {
        "category": result.get("category", "OTHER"),
        "confidence": float(result.get("confidence", 0.7)),
    }
