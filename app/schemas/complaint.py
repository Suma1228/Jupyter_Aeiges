from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel
from app.models.complaint import ComplaintCategory, ComplaintPriority, ComplaintStatus
from app.models.ai_analysis import SentimentType, SLARiskLevel


class ComplaintCreateRequest(BaseModel):
    title: str
    description: str
    policy_number: str | None = None


class AIAnalysisResponse(BaseModel):
    category: str
    priority: str
    assigned_team: str
    confidence: float
    reason: str
    suggested_action: str
    sentiment: str
    sla_risk: str
    explainability: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class TeamResponse(BaseModel):
    id: str
    name: str
    team_type: str

    model_config = {"from_attributes": True}


class ComplaintResponse(BaseModel):
    id: str
    complaint_number: str
    title: str
    description: str
    policy_number: str | None
    status: ComplaintStatus
    category: ComplaintCategory | None
    priority: ComplaintPriority | None
    sla_hours: int | None
    sla_due_at: datetime | None
    assigned_team: TeamResponse | None
    ai_analysis: AIAnalysisResponse | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ComplaintListItem(BaseModel):
    id: str
    complaint_number: str
    title: str
    status: ComplaintStatus
    category: ComplaintCategory | None
    priority: ComplaintPriority | None
    sla_due_at: datetime | None
    assigned_team: TeamResponse | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AssignRequest(BaseModel):
    team_id: str


class ResolveRequest(BaseModel):
    resolution_note: str | None = None


class DashboardResponse(BaseModel):
    total_complaints: int
    high_priority: int
    sla_risk_count: int
    resolved_today: int
