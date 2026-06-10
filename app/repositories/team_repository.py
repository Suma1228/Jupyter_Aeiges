from __future__ import annotations
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.team import Team, TeamType


class TeamRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, team_id: uuid.UUID) -> Team | None:
        result = await self.db.execute(select(Team).where(Team.id == team_id))
        return result.scalar_one_or_none()

    async def get_by_type(self, team_type: TeamType) -> Team | None:
        result = await self.db.execute(
            select(Team).where(Team.team_type == team_type)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Team | None:
        result = await self.db.execute(select(Team).where(Team.name == name))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Team]:
        result = await self.db.execute(select(Team))
        return list(result.scalars().all())
