# Phase 4 Plan: Infra and CI/CD

## Goal

Provide local integration orchestration and CI workflows that match repository commands and preserve debugging artifacts for AI agents.

## Scope

- Add `infra/compose.yml` to run PostgreSQL, backend, and frontend together.
- Add backend/frontend Dockerfiles for compose runtime.
- Add workflows:
  - `backend-ci.yml`
  - `frontend-ci.yml`
  - `integration-ci.yml`
  - `docs-guard.yml`
- Ensure CI checks include:
  - backend lint/format/typecheck/tests
  - Alembic upgrade head smoke
  - frontend lint/typecheck/test/build
  - Playwright smoke
  - docs link + command consistency
- Upload useful artifacts on failure paths.

## Assumptions

- GitHub Actions should use Python 3.13 to match local execution environment.
- Integration workflow can rely on service containers for PostgreSQL and ephemeral app processes.
- Docs guard can be implemented as a repository-local Python script.

## Verification

- YAML syntax sanity: `python -c "import yaml"` is optional; prefer workflow visual inspection.
- Local command checks:
  - `python scripts/docs_guard.py`
  - backend and frontend command parity against README.
