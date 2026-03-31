# Baseline Plan: Audit and Hardening

## Goal

Upgrade the repository from "generated scaffold" to "long-term AI coding baseline" by removing blocking inconsistencies and proving real execution paths.

## Scope

1. Governance and docs audit:
- Review root/backend/frontend `AGENTS.md` for brevity, layering clarity, and actionable validation rules.
- Verify `README.md`, `ARCHITECTURE.md`, `PLANS.md`, and generated docs against real repo behavior.
- Detect rules that are not mechanically verifiable and add/adjust checks where needed.

2. Runtime and quality audit:
- Backend: install, lint, typecheck, tests, migration, startup, `/health`, `/ready`.
- Frontend: install, lint, typecheck, tests, build, startup, `/playground`, Playwright smoke.
- Integration: minimal local backend+frontend+postgres orchestration check via compose config and runtime probing.

3. CI/CD alignment audit:
- Verify workflow commands match local documented commands.
- Ensure workflow artifact uploads aid AI troubleshooting.

4. Hardening pass:
- Fix blocking issues first (cannot install/run/verify, command mismatch, docs drift).
- Update docs and plans to reflect final executable state.

## Assumptions

- No business modules are introduced in this pass.
- Python and Node versions available locally may differ from CI but command semantics remain consistent.
- Local verification should prioritize reproducible command paths over visual/manual checks.

## Verification Matrix

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy app
pytest -q
DATABASE_URL=sqlite+pysqlite:///./tmp-alembic.db alembic upgrade head
python scripts/generate_db_schema.py
uvicorn app.main:app --host 127.0.0.1 --port 8000
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/ready
```

### Frontend

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
npm run dev -- --host 127.0.0.1 --port 5173
curl -fsS http://127.0.0.1:5173/playground
```

### Docs and Infra

```bash
python3 scripts/docs_guard.py
docker compose -f infra/compose.yml config
```

## Execution Notes

### Findings

1. Frontend install guidance was less deterministic (`npm install`), while CI uses `npm ci`.
2. Backend/README migration command relied on ambient PostgreSQL and was not deterministic for local smoke checks.
3. `docs_guard.py` did not verify workflow command parity or enforce AGENTS brevity.
4. `PLANS.md` did not reference this baseline hardening plan.

### Hardening Actions

1. Standardized local frontend install/validation docs to `npm ci --no-audit --no-fund`.
2. Standardized local Alembic smoke command to `DATABASE_URL=sqlite+pysqlite:///./tmp-alembic.db alembic upgrade head`.
3. Extended `scripts/docs_guard.py` with:
- AGENTS length guard.
- Workflow command parity checks.
- Baseline plan reference checks.
4. Updated `README.md`, `ARCHITECTURE.md`, `PLANS.md`, backend/frontend AGENTS, and phase plan docs for command consistency.

### Validation Outcome

- Backend lint/typecheck/tests/migrations/startup probes: passed.
- Frontend lint/typecheck/unit/build/playwright/startup: passed.
- Docs guard and compose config validation: passed.
- Compose runtime pull for `postgres:16-alpine`: blocked by local Docker DNS resolution to Docker Hub; minimal local integration fallback was executed and passed.
