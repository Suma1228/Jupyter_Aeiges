import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.team import Team, TeamType
from app.auth.utils import hash_password


SEED_TEAMS = [
    {"name": "Claims Operations Team", "team_type": TeamType.CLAIMS},
    {"name": "Property Assessment Team", "team_type": TeamType.SURVEYOR},
    {"name": "Policy Administration Team", "team_type": TeamType.POLICY_ADMIN},
    {"name": "Billing & Premium Team", "team_type": TeamType.BILLING},
    {"name": "Special Investigation Unit", "team_type": TeamType.FRAUD},
]

SEED_USERS = [
    {
        "name": "Test Customer",
        "email": "customer@test.com",
        "password": "password123",
        "role": UserRole.CUSTOMER,
    },
    {
        "name": "Ops Agent",
        "email": "ops@test.com",
        "password": "password123",
        "role": UserRole.OPS,
    },
]


async def seed_database():
    async with AsyncSessionLocal() as session:
        # Seed teams
        for team_data in SEED_TEAMS:
            result = await session.execute(
                select(Team).where(Team.team_type == team_data["team_type"])
            )
            existing = result.scalar_one_or_none()
            if not existing:
                team = Team(
                    id=uuid.uuid4(),
                    name=team_data["name"],
                    team_type=team_data["team_type"],
                )
                session.add(team)

        # Seed users
        for user_data in SEED_USERS:
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing = result.scalar_one_or_none()
            if not existing:
                user = User(
                    id=uuid.uuid4(),
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=hash_password(user_data["password"]),
                    role=user_data["role"],
                )
                session.add(user)

        await session.commit()
        print("✅ Database seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed_database())
