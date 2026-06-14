"""
Aegis Backend — AI Insurance Complaint Classification & Routing Engine
FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import engine, Base
from app.api import auth, complaints, ops
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables and seed on startup."""
    import app.models  # noqa: F401 — registers all models with Base metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.db.seed import seed_database
    await seed_database()

    yield

    await engine.dispose()


app = FastAPI(
    title="Aegis — AI Insurance Complaint Engine",
    description="AI-powered complaint classification, routing, and analysis backend.",
    version="1.0.0",
    lifespan=lifespan,
)


JUPYTER_ORIGIN = os.environ.get("JUPYTER_ORIGIN", "")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
]
if JUPYTER_ORIGIN:
    origins.append(JUPYTER_ORIGIN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(ops.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Aegis Backend",
        "version": "1.0.0",
        "llm_provider": settings.LLM_PROVIDER,
    }
