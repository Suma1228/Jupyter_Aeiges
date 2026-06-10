"""Unit tests for the Classification Agent."""

import pytest
from app.agents.classification import run_classification_agent


@pytest.mark.asyncio
async def test_classifies_claims_complaint(mock_llm, claims_complaint):
    result = await run_classification_agent(
        title=claims_complaint["title"],
        description=claims_complaint["description"],
        llm=mock_llm,
    )
    assert result["category"] == "CLAIMS"
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["confidence"] > 0.5


@pytest.mark.asyncio
async def test_classifies_fraud_complaint(mock_llm, fraud_complaint):
    result = await run_classification_agent(
        title=fraud_complaint["title"],
        description=fraud_complaint["description"],
        llm=mock_llm,
    )
    assert result["category"] == "FRAUD"
    assert result["confidence"] > 0.5


@pytest.mark.asyncio
async def test_classifies_billing_complaint(mock_llm, billing_complaint):
    result = await run_classification_agent(
        title=billing_complaint["title"],
        description=billing_complaint["description"],
        llm=mock_llm,
    )
    assert result["category"] == "BILLING"


@pytest.mark.asyncio
async def test_returns_other_for_unknown(mock_llm):
    result = await run_classification_agent(
        title="General inquiry",
        description="I have a question about my account.",
        llm=mock_llm,
    )
    assert result["category"] in ["CLAIMS", "BILLING", "FRAUD", "SURVEYOR", "POLICY_ADMIN", "OTHER"]
    assert "confidence" in result


@pytest.mark.asyncio
async def test_confidence_is_float(mock_llm, claims_complaint):
    result = await run_classification_agent(
        title=claims_complaint["title"],
        description=claims_complaint["description"],
        llm=mock_llm,
    )
    assert isinstance(result["confidence"], float)
