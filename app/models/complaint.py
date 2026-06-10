import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Enum as SAEnum, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.base import Base


class ComplaintCategory(str, enum.Enum):
    CLAIMS = "CLAIMS"
    SURVEYOR = "SURVEYOR"
    POLICY_ADMIN = "POLICY_ADMIN"
    BILLING = "BILLING"
    FRAUD = "FRAUD"
    OTHER = "OTHER"


class ComplaintPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ComplaintStatus(str, enum.Enum):
    NEW = "NEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    IN_PROGRESS = "IN_PROGRESS"
    AWAITING_CUSTOMER = "AWAITING_CUSTOMER"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    policy_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(
        SAEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.NEW
    )
    category: Mapped[ComplaintCategory | None] = mapped_column(SAEnum(ComplaintCategory), nullable=True)
    priority: Mapped[ComplaintPriority | None] = mapped_column(SAEnum(ComplaintPriority), nullable=True)
    assigned_team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True
    )
    sla_hours: Mapped[int | None] = mapped_column(nullable=True)
    sla_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    customer = relationship("User", foreign_keys=[customer_id])
    assigned_team = relationship("Team", foreign_keys=[assigned_team_id])
    ai_analysis = relationship("AIAnalysis", back_populates="complaint", uselist=False)
