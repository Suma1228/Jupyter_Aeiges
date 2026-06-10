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



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables and seed on startup."""
    # Import all models to register with Base metadata
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed database with initial data
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

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
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
