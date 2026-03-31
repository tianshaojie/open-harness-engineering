# Backend AGENTS

## Scope

Applies to everything under `backend/`.

## Rules

1. Keep backend architecture layered: `api -> services -> repositories`.
2. Maintain strict separation between transport schemas and persistence models.
3. No business domain modules in foundation stage.
4. Every backend change must keep `/health` and `/ready` meaningful.
5. Migrations must stay reproducible via Alembic.

## Required Validation

```bash
cd backend
ruff format --check .
ruff check .
mypy app
pytest -q
alembic upgrade head
```
