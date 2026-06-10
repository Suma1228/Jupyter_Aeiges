"""Unit tests for the Sentiment Agent."""

import pytest
from app.agents.sentiment import run_sentiment_agent

VALID_SENTIMENTS = {"POSITIVE", "NEUTRAL", "NEGATIVE"}


@pytest.mark.asyncio
async def test_negative_sentiment_for_angry_complaint(mock_llm):
    result = await run_sentiment_agent(
        title="Terrible service — worst experience",
        description="I am absolutely disgusted with the service. This is unacceptable. "
                    "I am escalating to the consumer court and will file a lawsuit.",
        llm=mock_llm,
    )
    assert result["sentiment"] == "NEGATIVE"


@pytest.mark.asyncio
async def test_positive_sentiment_for_satisfied_customer(mock_llm):
    result = await run_sentiment_agent(
        title="Thank you for quick resolution",
        description="I am happy and satisfied with the service. Great support team. "
                    "The resolution was excellent and I appreciate the help.",
        llm=mock_llm,
    )
    assert result["sentiment"] == "POSITIVE"


@pytest.mark.asyncio
async def test_neutral_sentiment_for_factual_inquiry(mock_llm):
    result = await run_sentiment_agent(
        title="Policy renewal query",
        description="I would like to know the renewal date for my policy number POL-12345. "
                    "Please provide the relevant details.",
        llm=mock_llm,
    )
    assert result["sentiment"] in VALID_SENTIMENTS


@pytest.mark.asyncio
async def test_sentiment_is_valid_value(mock_llm, claims_complaint):
    result = await run_sentiment_agent(
        title=claims_complaint["title"],
        description=claims_complaint["description"],
        llm=mock_llm,
    )
    assert result["sentiment"] in VALID_SENTIMENTS
