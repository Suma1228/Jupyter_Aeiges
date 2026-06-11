from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.user import User
from app.auth.dependencies import require_ops
from app.services.complaint_service import ComplaintService
from app.schemas.complaint import (
    ComplaintResponse,
    ComplaintListItem,
    AssignRequest,
    ResolveRequest,
    DashboardResponse,
)
from app.utils.serializers import complaint_to_response

router = APIRouter(prefix="/api/ops", tags=["Operations"])


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(
    current_user: User = Depends(require_ops),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    metrics = await service.get_dashboard_metrics()
    return DashboardResponse(**metrics)


@router.get("/complaints", response_model=list[ComplaintListItem])
async def list_complaints(
    current_user: User = Depends(require_ops),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaints = await service.get_all_complaints()
    return [complaint_to_response(c) for c in complaints]


@router.get("/complaints/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: uuid.UUID,
    current_user: User = Depends(require_ops),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaint = await service.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint_to_response(complaint)


@router.put("/complaints/{complaint_id}/assign", response_model=ComplaintResponse)
async def assign_complaint(
    complaint_id: uuid.UUID,
    payload: AssignRequest,
    current_user: User = Depends(require_ops),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    try:
        complaint = await service.assign_complaint(
            complaint_id=complaint_id,
            team_id=uuid.UUID(payload.team_id),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return complaint_to_response(complaint)


@router.put("/complaints/{complaint_id}/resolve", response_model=ComplaintResponse)
async def resolve_complaint(
    complaint_id: uuid.UUID,
    payload: ResolveRequest,
    current_user: User = Depends(require_ops),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    try:
        complaint = await service.resolve_complaint(complaint_id=complaint_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return complaint_to_response(complaint)