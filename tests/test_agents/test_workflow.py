"""Integration tests for the full Aegis LangGraph workflow."""

import pytest
from unittest.mock import patch
from app.agents.llm_provider import MockProvider
from app.agents.workflow import run_aegis_workflow, build_aegis_workflow


@pytest.mark.asyncio
async def test_full_workflow_claims_complaint(claims_complaint):
    """Full workflow should return all required fields for a claims complaint."""
    with patch("app.agents.workflow.get_llm_provider", return_value=MockProvider()):
        result = await run_aegis_workflow(
            title=claims_complaint["title"],
            description=claims_complaint["description"],
        )

    # All agents should have populated state
    assert result.get("category") is not None
    assert result.get("confidence") is not None
    assert result.get("priority") is not None
    assert result.get("assigned_team") is not None
    assert result.get("sentiment") is not None
    assert result.get("sla_risk") is not None
    assert result.get("sla_hours") is not None
    assert result.get("reason") is not None
    assert result.get("suggested_action") is not None

    # Claims complaint should classify correctly
    assert result["category"] == "CLAIMS"
    assert result["priority"] in ("HIGH", "MEDIUM", "CRITICAL")
    assert result["assigned_team"] == "Claims Operations Team"


@pytest.mark.asyncio
async def test_full_workflow_fraud_complaint(fraud_complaint):
    """Fraud complaint should route to Special Investigation Unit."""
    with patch("app.agents.workflow.get_llm_provider", return_value=MockProvider()):
        result = await run_aegis_workflow(
            title=fraud_complaint["title"],
            description=fraud_complaint["description"],
        )

    assert result["category"] == "FRAUD"
    assert result["assigned_team"] == "Special Investigation Unit"


@pytest.mark.asyncio
async def test_workflow_has_no_critical_errors(claims_complaint):
    """Workflow should complete without workflow-level errors on valid input."""
    with patch("app.agents.workflow.get_llm_provider", return_value=MockProvider()):
        result = await run_aegis_workflow(
            title=claims_complaint["title"],
            description=claims_complaint["description"],
        )

    # No agent errors on a valid complaint
    assert result.get("errors", []) == []


@pytest.mark.asyncio
async def test_workflow_sla_hours_matches_priority(critical_complaint):
    """SLA hours must match the SLA rules table."""
    with patch("app.agents.workflow.get_llm_provider", return_value=MockProvider()):
        result = await run_aegis_workflow(
            title=critical_complaint["title"],
            description=critical_complaint["description"],
        )

    priority = result.get("priority")
    sla_hours = result.get("sla_hours")
    sla_map = {"CRITICAL": 4, "HIGH": 24, "MEDIUM": 48, "LOW": 72}
    assert sla_hours == sla_map.get(priority)


@pytest.mark.asyncio
async def test_workflow_builds_without_error():
    """Workflow graph should compile without raising exceptions."""
    with patch("app.agents.workflow.get_llm_provider", return_value=MockProvider()):
        workflow = build_aegis_workflow(llm=MockProvider())
    assert workflow is not None
