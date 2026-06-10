import uuid
from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.base import Base


class TeamType(str, enum.Enum):
    CLAIMS = "CLAIMS"
    SURVEYOR = "SURVEYOR"
    POLICY_ADMIN = "POLICY_ADMIN"
    BILLING = "BILLING"
    FRAUD = "FRAUD"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    team_type: Mapped[TeamType] = mapped_column(SAEnum(TeamType), nullable=False, unique=True)
