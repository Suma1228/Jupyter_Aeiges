"""
Complaint Service — orchestrates complaint submission, AI workflow, and operations actions.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint, ComplaintStatus, ComplaintCategory, ComplaintPriority
from app.models.ai_analysis import AIAnalysis, SentimentType, SLARiskLevel
from app.models.team import TeamType
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.team_repository import TeamRepository
from app.agents.workflow import run_aegis_workflow
from app.agents.sla_risk import SLA_HOURS_MAP

CATEGORY_TO_TEAM_TYPE = {
    "CLAIMS": TeamType.CLAIMS,
    "SURVEYOR": TeamType.SURVEYOR,
    "POLICY_ADMIN": TeamType.POLICY_ADMIN,
    "BILLING": TeamType.BILLING,
    "FRAUD": TeamType.FRAUD,
    "OTHER": TeamType.CLAIMS,
}


class ComplaintService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.complaint_repo = ComplaintRepository(db)
        self.team_repo = TeamRepository(db)

    async def submit_complaint(
        self,
        customer_id: uuid.UUID,
        title: str,
        description: str,
        policy_number: str | None = None,
    ) -> Complaint:
        """
        Full complaint submission flow:
        1. Generate complaint number
        2. Save complaint (NEW status)
        3. Run Aegis AI workflow
        4. Update complaint with AI results
        5. Save AI analysis record
        6. Commit everything
        """
        # Step 1: Generate complaint number
        complaint_number = await self.complaint_repo.generate_complaint_number()

        # Step 2: Create complaint record
        complaint = Complaint(
            id=uuid.uuid4(),
            complaint_number=complaint_number,
            customer_id=customer_id,
            title=title,
            description=description,
            policy_number=policy_number,
            status=ComplaintStatus.UNDER_REVIEW,
        )
        complaint = await self.complaint_repo.create(complaint)

        # Step 3: Run AI workflow
        ai_state = await run_aegis_workflow(title=title, description=description)

        # Step 4: Resolve team from AI routing output
        category_str = ai_state.get("category", "OTHER")
        team_type = CATEGORY_TO_TEAM_TYPE.get(category_str, TeamType.CLAIMS)
        team = await self.team_repo.get_by_type(team_type)

        # Step 5: Update complaint with AI results
        priority_str = ai_state.get("priority", "MEDIUM")
        sla_hours = ai_state.get("sla_hours") or SLA_HOURS_MAP.get(priority_str, 48)

        complaint.category = ComplaintCategory(category_str) if category_str in ComplaintCategory.__members__ else ComplaintCategory.OTHER
        complaint.priority = ComplaintPriority(priority_str) if priority_str in ComplaintPriority.__members__ else ComplaintPriority.MEDIUM
        complaint.assigned_team_id = team.id if team else None
        complaint.sla_hours = sla_hours
        complaint.sla_due_at = datetime.now(timezone.utc) + timedelta(hours=sla_hours)
        complaint.status = ComplaintStatus.IN_PROGRESS

        # Step 6: Build explainability
        explainability = {
            "keywords": self._extract_keywords(title, description),
            "sentiment": ai_state.get("sentiment", "NEUTRAL").lower(),
            "sla_risk": ai_state.get("sla_risk", "MEDIUM").lower(),
            "category_confidence": round(ai_state.get("confidence", 0.7), 2),
            "workflow_errors": ai_state.get("errors", []),
        }

        # Step 7: Save AI analysis
        analysis = AIAnalysis(
            id=uuid.uuid4(),
            complaint_id=complaint.id,
            category=category_str,
            priority=priority_str,
            assigned_team=ai_state.get("assigned_team", "Claims Operations Team"),
            sentiment=SentimentType(ai_state.get("sentiment", "NEUTRAL")),
            sla_risk=SLARiskLevel(ai_state.get("sla_risk", "MEDIUM")),
            confidence=ai_state.get("confidence", 0.7),
            reason=ai_state.get("reason", "Analysis completed."),
            suggested_action=ai_state.get("suggested_action", "Review and resolve."),
            explainability=explainability,
        )
        await self.complaint_repo.save_ai_analysis(analysis)
        await self.complaint_repo.update(complaint)

        # Step 8: Commit transaction
        await self.db.commit()

        # Step 9: Re-fetch with relationships
        return await self.complaint_repo.get_by_id(complaint.id)

    async def get_my_complaints(self, customer_id: uuid.UUID) -> list[Complaint]:
        return await self.complaint_repo.get_by_customer(customer_id)

    async def get_complaint_by_id(self, complaint_id: uuid.UUID) -> Complaint | None:
        return await self.complaint_repo.get_by_id(complaint_id)

    async def get_all_complaints(self) -> list[Complaint]:
        return await self.complaint_repo.get_all()

    async def assign_complaint(
        self, complaint_id: uuid.UUID, team_id: uuid.UUID
    ) -> Complaint:
        complaint = await self.complaint_repo.get_by_id(complaint_id)
        if not complaint:
            raise ValueError(f"Complaint {complaint_id} not found")
        complaint.assigned_team_id = team_id
        complaint.status = ComplaintStatus.IN_PROGRESS
        await self.complaint_repo.update(complaint)
        await self.db.commit()
        return await self.complaint_repo.get_by_id(complaint_id)

    async def resolve_complaint(
        self, complaint_id: uuid.UUID
    ) -> Complaint:
        complaint = await self.complaint_repo.get_by_id(complaint_id)
        if not complaint:
            raise ValueError(f"Complaint {complaint_id} not found")
        complaint.status = ComplaintStatus.RESOLVED
        await self.complaint_repo.update(complaint)
        await self.db.commit()
        return await self.complaint_repo.get_by_id(complaint_id)

    async def get_dashboard_metrics(self) -> dict:
        return await self.complaint_repo.get_dashboard_metrics()

    def _extract_keywords(self, title: str, description: str) -> list[str]:
        """Simple keyword extraction for explainability."""
        from app.agents.llm_provider import (
            CLAIMS_KEYWORDS, BILLING_KEYWORDS, FRAUD_KEYWORDS,
            NEGATIVE_KEYWORDS, CRITICAL_KEYWORDS
        )
        all_keywords = CLAIMS_KEYWORDS + BILLING_KEYWORDS + FRAUD_KEYWORDS + NEGATIVE_KEYWORDS + CRITICAL_KEYWORDS
        text = f"{title} {description}".lower()
        found = [kw for kw in all_keywords if kw in text]
        return list(set(found))[:10]  # Top 10 unique keywords
