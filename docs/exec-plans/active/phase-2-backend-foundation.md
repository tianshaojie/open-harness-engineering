# Phase 2 Plan: Backend Foundation

## Goal

Build an AI-navigable FastAPI backend skeleton with PostgreSQL connectivity, Alembic migrations, health probes, and smoke test coverage.

## Scope

- Create `backend/` Python project metadata and dependency management.
- Establish layered app structure:
  - `app/core`
  - `app/api`
  - `app/models`
  - `app/schemas`
  - `app/repositories`
  - `app/services`
  - `app/tests`
- Configure PostgreSQL connection settings and DB session handling.
- Configure Alembic (`alembic.ini`, `alembic/env.py`, baseline revision).
- Implement `/health` and `/ready` probes.
- Add minimal structured JSON logging.
- Add minimal smoke tests.
- Generate `docs/generated/db-schema.md`.

## Assumptions

- Foundation stage should avoid domain/business entities.
- A technical baseline migration (non-domain) is acceptable to validate migration pipeline.
- Local smoke tests can use SQLite override for speed while runtime default remains PostgreSQL.

## Verification

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy app
pytest -q
alembic upgrade head
python scripts/generate_db_schema.py
```
