"""Unit tests for the LLM provider abstraction layer."""

import pytest
import json
from app.agents.llm_provider import MockProvider, get_llm_provider


@pytest.mark.asyncio
async def test_mock_provider_classify_system_prompt():
    """MockProvider should return valid category JSON for classification prompt."""
    provider = MockProvider()
    result = await provider.complete(
        system_prompt="classify the category of this insurance complaint",
        user_prompt="Complaint Title: Accident claim pending\nComplaint Description: My claim is pending for 20 days.",
    )
    data = json.loads(result)
    assert "category" in data
    assert "confidence" in data


@pytest.mark.asyncio
async def test_mock_provider_priority_system_prompt():
    """MockProvider should return valid priority JSON."""
    provider = MockProvider()
    result = await provider.complete(
        system_prompt="assign priority level to this complaint",
        user_prompt="Priority: HIGH\nComplaint: Fatal accident case.",
    )
    data = json.loads(result)
    assert "priority" in data
    assert data["priority"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


@pytest.mark.asyncio
async def test_mock_provider_sentiment_system_prompt():
    """MockProvider should return valid sentiment JSON."""
    provider = MockProvider()
    result = await provider.complete(
        system_prompt="analyze the sentiment of this complaint",
        user_prompt="Complaint Title: Worst service ever\nDescription: I am disgusted and angry.",
    )
    data = json.loads(result)
    assert "sentiment" in data
    assert data["sentiment"] in ("POSITIVE", "NEUTRAL", "NEGATIVE")


@pytest.mark.asyncio
async def test_mock_provider_complete_json():
    """complete_json should parse the JSON and return a dict."""
    provider = MockProvider()
    result = await provider.complete_json(
        system_prompt="classify the category of this insurance complaint",
        user_prompt="Complaint Title: Billing issue\nComplaint Description: I was overcharged premium.",
    )
    assert isinstance(result, dict)


def test_get_llm_provider_returns_mock_by_default(monkeypatch):
    """Factory should return MockProvider when LLM_PROVIDER=mock."""
    monkeypatch.setattr("app.agents.llm_provider.settings.LLM_PROVIDER", "mock")
    provider = get_llm_provider()
    assert isinstance(provider, MockProvider)


def test_get_llm_provider_raises_for_unknown(monkeypatch):
    """Factory should raise ValueError for unknown provider names."""
    monkeypatch.setattr("app.agents.llm_provider.settings.LLM_PROVIDER", "unknown_model")
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        get_llm_provider()
