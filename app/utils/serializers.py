"""
Serializers: convert SQLAlchemy model instances to Pydantic response schemas.
Centralizes all model → schema conversion logic.
"""

from __future__ import annotations
from app.models.complaint import Complaint
from app.models.ai_analysis import AIAnalysis
from app.schemas.complaint import ComplaintResponse, ComplaintListItem, AIAnalysisResponse, TeamResponse


def team_to_response(team) -> TeamResponse | None:
    if team is None:
        return None
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        team_type=team.team_type.value,
    )


def analysis_to_response(analysis: AIAnalysis) -> AIAnalysisResponse:
    return AIAnalysisResponse(
        category=analysis.category,
        priority=analysis.priority,
        assigned_team=analysis.assigned_team,
        confidence=round(analysis.confidence * 100, 1),  # Convert to percentage for frontend
        reason=analysis.reason,
        suggested_action=analysis.suggested_action,
        sentiment=analysis.sentiment.value,
        sla_risk=analysis.sla_risk.value,
        explainability=analysis.explainability,
    )


def complaint_to_response(complaint: Complaint) -> ComplaintResponse:
    return ComplaintResponse(
        id=str(complaint.id),
        complaint_number=complaint.complaint_number,
        title=complaint.title,
        description=complaint.description,
        policy_number=complaint.policy_number,
        status=complaint.status,
        category=complaint.category,
        priority=complaint.priority,
        sla_hours=complaint.sla_hours,
        sla_due_at=complaint.sla_due_at,
        assigned_team=team_to_response(complaint.assigned_team),
        ai_analysis=analysis_to_response(complaint.ai_analysis) if complaint.ai_analysis else None,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
    )
