# Aegis Backend

**AI Insurance Complaint Classification & Routing Engine**  
TCS × AMD AI Hackathon — Track 1: Agents

---

## What It Does

Customers submit insurance complaints. Aegis runs a **6-agent LangGraph pipeline** that automatically:

1. **Classifies** the complaint (Claims, Billing, Fraud, Policy, Survey)
2. **Assigns priority** (Critical → High → Medium → Low)
3. **Routes** to the correct operations team
4. **Analyzes sentiment** (Positive / Neutral / Negative)
5. **Predicts SLA risk** based on priority and sentiment
6. **Generates supervisor summary** with reason + suggested action

Results appear in the AI Analysis Panel for ops agents — zero manual triage.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| AI Orchestration | LangGraph + LangChain |
| LLM (default) | MockProvider (keyword-based, zero-latency) |
| Auth | JWT (access token only) |
| Validation | Pydantic v2 |
| Containers | Docker + Docker Compose |
| Tests | pytest + pytest-asyncio |

---

## Quick Start (Docker)

```bash
# 1. Clone and enter directory
git clone <repo>
cd aegis-backend

# 2. Copy env file (defaults are ready for Docker)
cp .env.example .env

# 3. Start everything
docker compose up --build

# 4. API is live at:
#    http://localhost:8000
#    http://localhost:8000/docs  ← Swagger UI
```

Database tables are auto-created and seeded on first startup. No migrations needed for initial run.

---

## Quick Start (Local Dev)

```bash
# Prerequisites: Python 3.12, PostgreSQL running locally

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set DATABASE_URL in .env to point to your local Postgres
cp .env.example .env            # Edit DATABASE_URL_SYNC for local

uvicorn app.main:app --reload
```

---

## Seed Users

| Email | Password | Role |
|---|---|---|
| `customer@test.com` | `password123` | CUSTOMER |
| `ops@test.com` | `password123` | OPS |

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | Login, returns JWT token |
| GET | `/api/auth/me` | Get current user info |

**Login request:**
```json
{ "email": "customer@test.com", "password": "password123" }
```

**Login response:**
```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

All subsequent requests: `Authorization: Bearer <token>`

---

### Customer APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/complaints` | Submit a new complaint (triggers AI pipeline) |
| GET | `/api/complaints/my` | List own complaints |
| GET | `/api/complaints/{id}` | Get complaint detail |
| GET | `/api/complaints/{id}/analysis` | Get AI analysis panel data |

**Submit complaint:**
```json
{
  "title": "Claim pending for 20 days — no update",
  "description": "I submitted my accident claim on Oct 1st...",
  "policy_number": "POL-2024-001234"
}
```

---

### Operations APIs (OPS role required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/ops/dashboard` | Dashboard metrics |
| GET | `/api/ops/complaints` | Full complaint queue |
| GET | `/api/ops/complaints/{id}` | Complaint + AI analysis |
| PUT | `/api/ops/complaints/{id}/assign` | Reassign to team |
| PUT | `/api/ops/complaints/{id}/resolve` | Mark resolved |

---

### AI Analysis Panel Response

```json
{
  "category": "CLAIMS",
  "priority": "HIGH",
  "assigned_team": "Claims Operations Team",
  "confidence": 94.0,
  "reason": "Claims complaint with significant urgency. Customer reports substantial delays or significant loss.",
  "suggested_action": "Assign to senior claims officer. Review claim status within 4 hours and provide customer update.",
  "sentiment": "NEGATIVE",
  "sla_risk": "HIGH",
  "explainability": {
    "keywords": ["claim", "pending", "accident"],
    "sentiment": "negative",
    "sla_risk": "high",
    "category_confidence": 0.94
  }
}
```

---

## LangGraph Workflow

```
[Complaint Submitted]
        │
        ▼
┌─────────────────┐
│  Classification │  → category + confidence
│      Agent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Priority     │  → LOW / MEDIUM / HIGH / CRITICAL
│      Agent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Routing      │  → assigned_team
│      Agent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Sentiment    │  → POSITIVE / NEUTRAL / NEGATIVE
│      Agent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    SLA Risk     │  → sla_risk + sla_hours
│      Agent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Supervisor    │  → reason + suggested_action
│      Agent      │
└────────┬────────┘
         │
         ▼
  [AI Analysis Saved]
```

Each node is a separate async function. State is passed through the graph as a `TypedDict`. Any node that fails degrades gracefully with sensible defaults — the pipeline always completes.

---

## SLA Rules

| Priority | SLA Hours |
|---|---|
| CRITICAL | 4 hours |
| HIGH | 24 hours |
| MEDIUM | 48 hours |
| LOW | 72 hours |

---

## Teams & Routing

| Category | Team |
|---|---|
| CLAIMS | Claims Operations Team |
| SURVEYOR | Property Assessment Team |
| POLICY_ADMIN | Policy Administration Team |
| BILLING | Billing & Premium Team |
| FRAUD | Special Investigation Unit |

---

## AMD GPU Integration (Future)

The entire AI layer is behind a `LLMProvider` abstraction in `app/agents/llm_provider.py`.

**To switch from Mock → AMD GPU model:**

```bash
# In .env:
LLM_PROVIDER=qwen
AMD_API_URL=http://your-amd-gpu-host:8080
```

That's it. No agent logic changes required. Stub implementations exist for:
- `QwenProvider` — Qwen 2.5 on ROCm
- `LlamaProvider` — Llama 3.x via vLLM / Ollama
- `DeepSeekProvider` — DeepSeek API or self-hosted

All use the same OpenAI-compatible chat completions endpoint format.

---

## Running Tests

```bash
# All tests (requires installed deps)
pytest

# Agent unit tests only (fast, no DB required)
pytest tests/test_agents/ -v

# With coverage
pytest --cov=app tests/
```

Tests use the real `MockProvider` — fully deterministic, no mocking of LLM calls needed for agent tests.

---

## Project Structure

```
aegis-backend/
├── app/
│   ├── agents/
│   │   ├── llm_provider.py      # LLM abstraction + MockProvider + AMD stubs
│   │   ├── classification.py    # Category + confidence
│   │   ├── priority.py          # Priority level
│   │   ├── routing.py           # Team assignment
│   │   ├── sentiment.py         # Customer sentiment
│   │   ├── sla_risk.py          # SLA breach prediction
│   │   ├── supervisor.py        # Synthesis + suggested actions
│   │   └── workflow.py          # LangGraph graph definition
│   ├── api/
│   │   ├── auth.py              # Login + me
│   │   ├── complaints.py        # Customer complaint APIs
│   │   └── ops.py               # Operations team APIs
│   ├── auth/
│   │   ├── utils.py             # JWT + password hashing
│   │   └── dependencies.py      # FastAPI auth deps
│   ├── core/
│   │   └── config.py            # Pydantic settings
│   ├── db/
│   │   ├── base.py              # Async engine + session
│   │   └── seed.py              # Seed users + teams
│   ├── models/                  # SQLAlchemy ORM models
│   ├── repositories/            # DB access layer
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── services/
│   │   └── complaint_service.py # Business logic orchestration
│   ├── utils/
│   │   └── serializers.py       # Model → schema converters
│   └── main.py                  # FastAPI app + lifespan
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── test_agents/             # Unit tests per agent
│   └── test_api/                # API endpoint tests
├── alembic/                     # DB migrations
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── pytest.ini
```

---

## Health Check

```
GET /health
→ { "status": "healthy", "service": "Aegis Backend", "llm_provider": "mock" }
```
