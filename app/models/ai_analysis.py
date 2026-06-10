import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Enum as SAEnum, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.base import Base


class SentimentType(str, enum.Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"


class SLARiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=False, unique=True, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    assigned_team: Mapped[str] = mapped_column(String(255), nullable=False)
    sentiment: Mapped[SentimentType] = mapped_column(SAEnum(SentimentType), nullable=False)
    sla_risk: Mapped[SLARiskLevel] = mapped_column(SAEnum(SLARiskLevel), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    suggested_action: Mapped[str] = mapped_column(String(1000), nullable=False)
    explainability: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    complaint = relationship("Complaint", back_populates="ai_analysis")
