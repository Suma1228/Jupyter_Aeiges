from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.complaint_service import ComplaintService
from app.schemas.complaint import (
    ComplaintCreateRequest,
    ComplaintResponse,
    ComplaintListItem,
    AIAnalysisResponse,
)
from app.utils.serializers import complaint_to_response, analysis_to_response

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def submit_complaint(
    payload: ComplaintCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaint = await service.submit_complaint(
        customer_id=current_user.id,
        title=payload.title,
        description=payload.description,
        policy_number=payload.policy_number,
    )
    return complaint_to_response(complaint)


@router.get("/my", response_model=list[ComplaintListItem])
async def my_complaints(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaints = await service.get_my_complaints(current_user.id)
    return [complaint_to_response(c) for c in complaints]


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaint = await service.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Customers can only view their own complaints
    from app.models.user import UserRole
    if current_user.role == UserRole.CUSTOMER and complaint.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return complaint_to_response(complaint)


@router.get("/{complaint_id}/analysis", response_model=AIAnalysisResponse)
async def get_complaint_analysis(
    complaint_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ComplaintService(db)
    complaint = await service.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    from app.models.user import UserRole
    if current_user.role == UserRole.CUSTOMER and complaint.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    if not complaint.ai_analysis:
        raise HTTPException(status_code=404, detail="AI analysis not yet available")

    return analysis_to_response(complaint.ai_analysis)
