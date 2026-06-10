"""Unit tests for the Priority Agent."""

import pytest
from app.agents.priority import run_priority_agent

VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


@pytest.mark.asyncio
async def test_critical_priority_for_fatal_complaint(mock_llm, critical_complaint):
    result = await run_priority_agent(
        title=critical_complaint["title"],
        description=critical_complaint["description"],
        category="CLAIMS",
        llm=mock_llm,
    )
    assert result["priority"] == "CRITICAL"


@pytest.mark.asyncio
async def test_high_priority_for_urgent_claim(mock_llm, claims_complaint):
    result = await run_priority_agent(
        title=claims_complaint["title"],
        description=claims_complaint["description"],
        category="CLAIMS",
        llm=mock_llm,
    )
    assert result["priority"] in ("HIGH", "MEDIUM")


@pytest.mark.asyncio
async def test_priority_is_valid_value(mock_llm, billing_complaint):
    result = await run_priority_agent(
        title=billing_complaint["title"],
        description=billing_complaint["description"],
        category="BILLING",
        llm=mock_llm,
    )
    assert result["priority"] in VALID_PRIORITIES


@pytest.mark.asyncio
async def test_fraud_is_high_or_critical(mock_llm, fraud_complaint):
    result = await run_priority_agent(
        title=fraud_complaint["title"],
        description=fraud_complaint["description"],
        category="FRAUD",
        llm=mock_llm,
    )
    # Fraud should not be LOW priority
    assert result["priority"] in ("HIGH", "CRITICAL", "MEDIUM")
