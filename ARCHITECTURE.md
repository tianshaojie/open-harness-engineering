# Architecture: open_harness_engineering

## 1. Repository Philosophy

This repository follows Harness Engineering principles:

1. **Docs are system of record**: if behavior changes, docs change in the same PR.
2. **AI-first execution**: AI agents implement most code/config; humans set constraints and direction.
3. **Plan before non-trivial coding**: complex work starts with an execution plan in `docs/exec-plans/active/`.
4. **Verification as gate**: each phase must run focused checks and report results/risks.
5. **Backend/frontend split governance**: separate agent rules and quality gates, shared repo-level harness standards.

## 2. Directory Responsibilities

- `AGENTS.md` repository-level guardrails and execution loop.
- `README.md` operator-facing setup and verification entrypoint.
- `PLANS.md` phase roadmap and status.
- `docs/design-docs/` durable design decisions and technical rationale.
- `docs/exec-plans/active/` current implementation plans for active work.
- `docs/runbooks/` operational procedures for humans/agents.
- `docs/generated/` generated inventories (schema/UI inventory) and machine-written summaries.
- `backend/` FastAPI service, migrations, and backend tests.
- `frontend/` Vue app shell (sidebar/topbar/content), UI system seed, and frontend tests.
- `infra/` local orchestration and runtime bootstrapping assets.
- `.github/workflows/` CI/CD for backend, frontend, integration, and docs guard.

## 3. Verification Strategy

### Backend

- static: `ruff format --check`, `ruff check`, `mypy`
- tests: `pytest`
- migration safety: `DATABASE_URL=sqlite+pysqlite:///./tmp-alembic.db alembic upgrade head`
- runtime probes: `GET /health`, `GET /ready`

### Frontend

- static: `npm run lint`, `npm run typecheck`
- unit tests: `npm run test`
- build correctness: `npm run build`
- runtime smoke: `npx playwright install chromium` + Playwright `/playground` check

### Repository and Docs

- command/link consistency checks via `python scripts/docs_guard.py`
- workflow command parity checks via `python scripts/docs_guard.py`
- AGENTS size guard (short, navigable docs) via `python scripts/docs_guard.py`
- generated docs refreshed after structural changes

## 4. AI Working Loop

1. Read relevant `AGENTS.md` and docs for the target area.
2. Write/refresh an execution plan in `docs/exec-plans/active/` for non-trivial tasks.
3. Implement in small, reviewable increments.
4. Run scoped validations and capture outputs/failures.
5. Update docs (`README`, generated docs, runbooks, plans) to match reality.
6. Self-review for naming, navigability, testability, and observability.

## 5. Assumption Logging Rule

When information is missing, proceed with explicit assumptions and record them in plan docs or phase summaries rather than blocking for confirmation.
