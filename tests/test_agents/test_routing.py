"""Unit tests for the Routing Agent."""

import pytest
from app.agents.routing import run_routing_agent


@pytest.mark.asyncio
async def test_routes_claims_to_claims_team(mock_llm):
    result = await run_routing_agent(
        category="CLAIMS",
        title="Claim issue",
        description="I have a pending claim.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Claims Operations Team"
    assert result["team_type"] == "CLAIMS"


@pytest.mark.asyncio
async def test_routes_fraud_to_siu(mock_llm):
    result = await run_routing_agent(
        category="FRAUD",
        title="Fraud suspected",
        description="Suspicious activity on my policy.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Special Investigation Unit"
    assert result["team_type"] == "FRAUD"


@pytest.mark.asyncio
async def test_routes_billing_to_billing_team(mock_llm):
    result = await run_routing_agent(
        category="BILLING",
        title="Premium overcharge",
        description="I was overcharged.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Billing & Premium Team"


@pytest.mark.asyncio
async def test_routes_surveyor_to_property_team(mock_llm):
    result = await run_routing_agent(
        category="SURVEYOR",
        title="Survey delay",
        description="Survey not done yet.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Property Assessment Team"


@pytest.mark.asyncio
async def test_routes_policy_admin(mock_llm):
    result = await run_routing_agent(
        category="POLICY_ADMIN",
        title="Policy document issue",
        description="Need policy certificate.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Policy Administration Team"


@pytest.mark.asyncio
async def test_routes_other_to_default(mock_llm):
    result = await run_routing_agent(
        category="OTHER",
        title="General issue",
        description="Something else.",
        llm=mock_llm,
    )
    assert result["assigned_team"] == "Claims Operations Team"
