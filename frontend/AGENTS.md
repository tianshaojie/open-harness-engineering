# Frontend AGENTS

## Scope

Applies to everything under `frontend/`.

## Rules

1. Keep app shell, routing, layout, and UI primitives clearly separated.
2. `components/ui` hosts reusable primitives; `components/shared` hosts app-level reuse.
3. No business pages/modules in foundation stage; use `/playground` for smoke interactions.
4. Theme tokens and layout should be easy for AI agents to discover and modify.
5. Every structural UI change must preserve Playwright smoke coverage.

## Required Validation

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
