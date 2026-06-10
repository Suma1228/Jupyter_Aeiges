"""Sentiment Agent — analyzes emotional tone of the complaint."""

from app.agents.llm_provider import LLMProvider

SYSTEM_PROMPT = """You are a sentiment analysis expert for insurance complaints.
Determine the overall sentiment expressed in the complaint.

Sentiment levels:
- POSITIVE: customer is satisfied, grateful, or complimentary
- NEUTRAL: factual, informational tone without strong emotions
- NEGATIVE: frustrated, angry, disappointed, threatening legal action

Respond ONLY with a JSON object, no markdown:
{"sentiment": "<POSITIVE|NEUTRAL|NEGATIVE>"}"""


async def run_sentiment_agent(
    title: str, description: str, llm: LLMProvider
) -> dict:
    """
    Analyzes the sentiment of a complaint.

    Returns:
        {"sentiment": str}
    """
    user_prompt = f"Complaint Title: {title}\n\nComplaint Description: {description}"
    result = await llm.complete_json(SYSTEM_PROMPT, user_prompt)
    sentiment = result.get("sentiment", "NEUTRAL").upper()
    if sentiment not in ("POSITIVE", "NEUTRAL", "NEGATIVE"):
        sentiment = "NEUTRAL"
    return {"sentiment": sentiment}
