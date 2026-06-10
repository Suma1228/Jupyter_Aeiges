"""
Pytest configuration and shared fixtures for Aegis backend tests.
"""

import asyncio
import uuid
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from app.agents.llm_provider import MockProvider


# ---------------------------------------------------------------------------
# Event loop
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ---------------------------------------------------------------------------
# LLM fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_llm():
    """Returns the real MockProvider (keyword-based, deterministic)."""
    return MockProvider()


# ---------------------------------------------------------------------------
# Sample complaint data
# ---------------------------------------------------------------------------

@pytest.fixture
def claims_complaint():
    return {
        "title": "Claim pending for 20 days — no response",
        "description": (
            "I submitted my accident claim 20 days ago but have not received any update. "
            "The claim number is CLM-2024-001. I am extremely frustrated and require "
            "immediate assistance to resolve this pending claim."
        ),
    }


@pytest.fixture
def fraud_complaint():
    return {
        "title": "Unauthorized policy modification suspected fraud",
        "description": (
            "I noticed that my policy details were changed without my consent. "
            "There appears to be a fraudulent impersonation attempt. "
            "Someone has forged documents and made unauthorized changes to my policy."
        ),
    }


@pytest.fixture
def billing_complaint():
    return {
        "title": "Overcharged premium amount in October",
        "description": (
            "I was charged an extra premium of Rs 2500 in October. "
            "The billing statement shows incorrect amount. "
            "Please issue a refund for the overcharged amount immediately."
        ),
    }


@pytest.fixture
def critical_complaint():
    return {
        "title": "Fatal accident — life insurance claim urgent",
        "description": (
            "My father was in a fatal accident and passed away. "
            "We need to file a life insurance claim as a matter of urgency. "
            "This is a life-threatening matter that requires immediate attention. "
            "Please help us process the death claim."
        ),
    }
