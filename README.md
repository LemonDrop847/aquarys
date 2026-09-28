# AQUARYS

Trust-aware environmental intelligence for urban streams and river restoration governance. AQUARYS validates whether stream observation evidence deserves to be believed, fingerprints multi-dimensional stream ecologies across 8 axes, discovers ecological twins, interrogates stream recovery hypotheses via the Oracle and Skeptic challenge engine, visualizes evidence provenance graphs, and coordinates volunteer data-collection missions.

## Project Structure

- `/` — Frontend Next.js application
- `/backend` — Backend FastAPI application

## Environment Setup

1. **Frontend**: Create a `.env` file in the root directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_DEMO_MODE=true
   ```

2. **Backend**: Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///aquarys.db
   OAH_BASE_URL=https://api.enora-oah.eu
   OAH_API_KEY=
   APP_MODE=demo
   LLM_PROVIDER=demo
   GEMINI_API_KEY=
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   CORS_ORIGINS=http://localhost:3000
   ```
   *See `env.example` or `backend/env.example` for details.*

## How to Run

### 1. Start Backend

```bash
cd backend
python -m uv sync
python -m uv run uvicorn aquarys.main:app --reload --port 8000
```

### 2. Start Frontend

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.
