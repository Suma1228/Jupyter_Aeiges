from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from app.models.complaint import Complaint, ComplaintStatus, ComplaintPriority
from app.models.ai_analysis import AIAnalysis


class ComplaintRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, complaint: Complaint) -> Complaint:
        self.db.add(complaint)
        await self.db.flush()
        await self.db.refresh(complaint)
        return complaint

    async def get_by_id(self, complaint_id: uuid.UUID) -> Complaint | None:
        result = await self.db.execute(
            select(Complaint)
            .where(Complaint.id == complaint_id)
            .options(
                selectinload(Complaint.assigned_team),
                selectinload(Complaint.ai_analysis),
                selectinload(Complaint.customer),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_customer(self, customer_id: uuid.UUID) -> list[Complaint]:
        result = await self.db.execute(
            select(Complaint)
            .where(Complaint.customer_id == customer_id)
            .options(
                selectinload(Complaint.assigned_team),
                selectinload(Complaint.ai_analysis),
            )
            .order_by(Complaint.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Complaint]:
        result = await self.db.execute(
            select(Complaint)
            .options(
                selectinload(Complaint.assigned_team),
                selectinload(Complaint.ai_analysis),
                selectinload(Complaint.customer),
            )
            .order_by(Complaint.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def update(self, complaint: Complaint) -> Complaint:
        complaint.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.refresh(complaint)
        return complaint

    async def save_ai_analysis(self, analysis: AIAnalysis) -> AIAnalysis:
        self.db.add(analysis)
        await self.db.flush()
        return analysis

    async def get_dashboard_metrics(self) -> dict:
        today_start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        total = await self.db.scalar(select(func.count(Complaint.id)))

        high_priority = await self.db.scalar(
            select(func.count(Complaint.id)).where(
                Complaint.priority.in_([ComplaintPriority.HIGH, ComplaintPriority.CRITICAL])
            )
        )

        sla_risk_count = await self.db.scalar(
            select(func.count(AIAnalysis.id)).where(AIAnalysis.sla_risk == "HIGH")
        )

        resolved_today = await self.db.scalar(
            select(func.count(Complaint.id)).where(
                and_(
                    Complaint.status == ComplaintStatus.RESOLVED,
                    Complaint.updated_at >= today_start,
                )
            )
        )

        return {
            "total_complaints": total or 0,
            "high_priority": high_priority or 0,
            "sla_risk_count": sla_risk_count or 0,
            "resolved_today": resolved_today or 0,
        }

    async def generate_complaint_number(self) -> str:
        count = await self.db.scalar(select(func.count(Complaint.id)))
        return f"AEGIS-{(count or 0) + 1:05d}"
