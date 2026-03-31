# open_harness_engineering

AI-native monorepo scaffold aligned with Harness Engineering principles.

## What This Repository Is

`open_harness_engineering` is a full-stack scaffold where AI agents do most implementation work while humans define rules, guardrails, and direction.

- `docs` is the system of record.
- backend and frontend are governed separately but follow shared repository harness rules.
- every non-trivial change should be planned, implemented, verified, and documented.

## Repository Layout

- `backend/` FastAPI + PostgreSQL + Alembic foundation.
- `frontend/` Vue 3 + TypeScript + Vite + shadcn/vue foundation.
- `infra/` local runtime orchestration assets.
- `docs/` architecture, plans, runbooks, generated inventories.
- `.github/workflows/` CI/CD pipelines.

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm ci --no-audit --no-fund
npm run dev
```

### Local Integration (Docker Compose)

```bash
docker compose -f infra/compose.yml up --build
```

## Verification Commands

### Backend Verification

```bash
cd backend
ruff format --check .
ruff check .
mypy app
pytest -q
DATABASE_URL=sqlite+pysqlite:///./tmp-alembic.db alembic upgrade head
python scripts/generate_db_schema.py
```

### Frontend Verification

```bash
cd frontend
npm ci --no-audit --no-fund
npm run lint
npm run typecheck
npm run test
npm run build
npx playwright install chromium
npm run test:e2e
npm run generate:ui-inventory
```

### Runtime Smoke (Recommended)

```bash
# backend
cd backend
source .venv/bin/activate
DATABASE_URL=sqlite+pysqlite:///./runtime-check.db uvicorn app.main:app --host 127.0.0.1 --port 18000
# then in another terminal:
curl -fsS http://127.0.0.1:18000/health
curl -fsS http://127.0.0.1:18000/ready

# frontend
cd frontend
npm run dev -- --host 127.0.0.1 --port 15173
# then in another terminal:
curl -fsS http://127.0.0.1:15173/playground
```

### Docs Guard

```bash
python scripts/docs_guard.py
```

## Core Documents

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [PLANS.md](PLANS.md)
- [Root Agent Rules](AGENTS.md)
- [Backend Agent Rules](backend/AGENTS.md)
- [Frontend Agent Rules](frontend/AGENTS.md)
