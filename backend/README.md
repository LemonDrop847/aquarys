# AQUARYS Backend

Trust-aware environmental intelligence backend for urban stream evidence reasoning, twin search, and mission optimization.

## Stack

- FastAPI
- PostgreSQL + PostGIS + pgvector
- SQLAlchemy 2.0 & Alembic
- Pydantic v2
- NumPy / Pandas / SciPy / scikit-learn
- Shapely & GeoAlchemy2

## Setup

```bash
cd backend
python -m uv sync
```

## Run

```bash
python -m uv run uvicorn aquarys.main:app --reload --port 8000
```

## Environment

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aquarys
OAH_BASE_URL=https://api.enora-oah.eu
OAH_API_KEY=
APP_MODE=demo
LLM_PROVIDER=demo
GEMINI_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
CORS_ORIGINS=http://localhost:3000
```

## API

- `GET /health` — Service health status
- `GET /sites`, `GET /sites/{id}`, `GET /sites/{id}/timeline` — Stream research sites & sensor history
- `GET /observations`, `GET /observations/{id}` — Citizen & sensor observations
- `POST /trust/evaluate`, `GET /observations/{id}/evidence` — Evidence trust passport evaluation
- `POST /twins/search`, `GET /twins/{site_a}/{site_b}` — Ecological twin matching & comparative trajectory
- `POST /oracle/investigate`, `POST /oracle/challenge` — Evidence-grounded Oracle & Skeptic investigation
- `POST /missions/optimize`, `GET /missions/{id}` — Information-gain mission optimizer
- `GET /exports/fhir/{investigation_id}` — Standard FHIR Bundle export
