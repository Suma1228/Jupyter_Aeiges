"""
Aegis LangGraph Workflow

Orchestrates the multi-agent pipeline:
  Classification → Priority → Routing → Sentiment → SLA Risk → Supervisor

Each node is a discrete agent. State flows through the graph.
"""

from __future__ import annotations
from typing import TypedDict, Any
from langgraph import graph
from langgraph.graph import StateGraph, END

from app.agents.llm_provider import LLMProvider, get_llm_provider
from app.agents.classification import run_classification_agent
from app.agents.priority import run_priority_agent
from app.agents.routing import run_routing_agent
from app.agents.sentiment import run_sentiment_agent
from app.agents.sla_risk import run_sla_risk_agent
from app.agents.supervisor import run_supervisor_agent




# ---------------------------------------------------------------------------
# Workflow State
# ---------------------------------------------------------------------------

class AegisState(TypedDict, total=False):
    # Inputs
    title: str
    description: str

    # Classification Agent output
    category: str
    confidence: float

    # Priority Agent output
    priority: str

    # Routing Agent output
    assigned_team: str
    team_type: str

    # Sentiment Agent output
    sentiment: str

    # SLA Risk Agent output
    sla_risk: str
    sla_hours: int

    # Supervisor Agent output
    reason: str
    suggested_action: str

    # Error tracking
    errors: list[str]


# ---------------------------------------------------------------------------
# Node functions (async)
# ---------------------------------------------------------------------------

def make_classification_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_classification_agent(
                title=state["title"],
                description=state["description"],
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {**state, "category": "OTHER", "confidence": 0.5, "errors": errors + [f"classification: {e}"]}
    return node


def make_priority_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_priority_agent(
                title=state["title"],
                description=state["description"],
                category=state.get("category", "OTHER"),
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {**state, "priority": "MEDIUM", "errors": errors + [f"priority: {e}"]}
    return node


def make_routing_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_routing_agent(
                category=state.get("category", "OTHER"),
                title=state["title"],
                description=state["description"],
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {**state, "assigned_team": "Claims Operations Team", "team_type": "CLAIMS", "errors": errors + [f"routing: {e}"]}
    return node


def make_sentiment_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_sentiment_agent(
                title=state["title"],
                description=state["description"],
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {**state, "sentiment": "NEUTRAL", "errors": errors + [f"sentiment: {e}"]}
    return node


def make_sla_risk_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_sla_risk_agent(
                priority=state.get("priority", "MEDIUM"),
                sentiment=state.get("sentiment", "NEUTRAL"),
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {**state, "sla_risk": "MEDIUM", "sla_hours": 48, "errors": errors + [f"sla_risk: {e}"]}
    return node


def make_supervisor_node(llm: LLMProvider):
    async def node(state: AegisState) -> AegisState:
        try:
            result = await run_supervisor_agent(
                title=state["title"],
                description=state["description"],
                category=state.get("category", "OTHER"),
                priority=state.get("priority", "MEDIUM"),
                assigned_team=state.get("assigned_team", "Claims Operations Team"),
                sentiment=state.get("sentiment", "NEUTRAL"),
                sla_risk=state.get("sla_risk", "MEDIUM"),
                confidence=state.get("confidence", 0.7),
                llm=llm,
            )
            return {**state, **result}
        except Exception as e:
            errors = state.get("errors", [])
            return {
                **state,
                "reason": "Automated analysis completed.",
                "suggested_action": "Please review and take appropriate action.",
                "errors": errors + [f"supervisor: {e}"],
            }
    return node


# ---------------------------------------------------------------------------
# Graph Builder
# ---------------------------------------------------------------------------

def build_aegis_workflow(llm: LLMProvider | None = None) -> StateGraph:
    """Constructs and compiles the Aegis LangGraph workflow."""
    if llm is None:
        llm = get_llm_provider()

    graph = StateGraph(AegisState)

    # Add nodes
    graph.add_node("classification_agent", make_classification_node(llm))
    graph.add_node("priority_agent", make_priority_node(llm))
    graph.add_node("routing_agent", make_routing_node(llm))
    graph.add_node("sentiment_agent", make_sentiment_node(llm))
    graph.add_node("sla_risk_agent", make_sla_risk_node(llm))
    graph.add_node("supervisor_agent", make_supervisor_node(llm))

    # Define edges (sequential pipeline)
    # Define edges (sequential pipeline)
    graph.set_entry_point("classification_agent")

    graph.add_edge("classification_agent", "priority_agent")
    graph.add_edge("priority_agent", "routing_agent")
    graph.add_edge("routing_agent", "sentiment_agent")
    graph.add_edge("sentiment_agent", "sla_risk_agent")
    graph.add_edge("sla_risk_agent", "supervisor_agent")
    graph.add_edge("supervisor_agent", END)

    return graph.compile()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

async def run_aegis_workflow(title: str, description: str) -> AegisState:
    """
    Runs the complete Aegis multi-agent workflow for a complaint.

    Args:
        title: Complaint title
        description: Complaint description

    Returns:
        Final AegisState with all agent outputs populated.
    """
    workflow = build_aegis_workflow()
    initial_state: AegisState = {
        "title": title,
        "description": description,
        "errors": [],
    }
    final_state = await workflow.ainvoke(initial_state)
    return final_state
