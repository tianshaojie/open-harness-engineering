# Plan: shadcn-admin Foundation Integration

## Goal

Integrate the shadcn-admin basic UI shell and foundational workspace structure into `frontend/` while preserving repository harness rules and non-business scope.

## Scope

1. Inspect upstream `satnaing/shadcn-admin` and identify reusable foundation pieces:
- app layout shell (sidebar/header/content)
- theme/style tokens and utility classes
- basic navigation information architecture
- core shared UI primitives used by the shell

2. Adapt into local project structure:
- keep existing repo conventions (`pages`, `components/ui`, `components/shared`, `components/playground`)
- keep `/playground` route available and reachable
- avoid adding business-domain modules or data

3. Hardening and documentation:
- update generated UI inventory
- update README/ARCHITECTURE/PLANS if commands or structure expectations change
- keep AGENTS constraints satisfied

## Assumptions

- Integration focuses on foundation visual shell and reusable UI space, not full upstream feature parity.
- Upstream licensing permits source-based adaptation for this repository usage.
- Existing frontend toolchain (Vue 3 + Vite + shadcn/vue style) remains unchanged.

## Verification

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

# runtime smoke
npm run dev -- --host 127.0.0.1 --port 15173
curl -fsS http://127.0.0.1:15173/
curl -fsS http://127.0.0.1:15173/playground

cd ..
python3 scripts/docs_guard.py
```

## Execution Notes

- Implemented a Vue-native adaptation of shadcn-admin foundation shell:
  - sidebar navigation groups
  - sticky top bar with route title and theme mode toggle
  - card-style content workspace container
- Kept route scope non-business (`/`, `/playground`, `404`) and preserved playground smoke interactions.
- Refreshed generated UI inventory after structure updates.

## Verification Results

- `npm ci --no-audit --no-fund`: passed
- `npm run lint`: passed (after replacing `localStorage` with `window.localStorage`)
- `npm run typecheck`: passed
- `npm run test`: passed
- `npm run build`: passed
- `npx playwright install chromium`: passed
- `npm run test:e2e`: passed
- `npm run generate:ui-inventory`: passed
- Runtime smoke:
  - requested `15173` was occupied; Vite auto-switched to `15174`
  - `curl -fsS http://127.0.0.1:15174/`: passed
  - `curl -fsS http://127.0.0.1:15174/playground`: passed
