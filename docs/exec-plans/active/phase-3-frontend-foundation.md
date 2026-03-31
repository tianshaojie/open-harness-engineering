# Phase 3 Plan: Frontend Foundation

## Goal

Build a Vue 3 + TypeScript + Vite frontend foundation with shadcn/vue-style UI primitives, app shell/routing/layout/theme, playground route, and smoke automation.

## Scope

- Initialize frontend project metadata and toolchain config.
- Create app shell with router and layout wiring.
- Add directory scaffold:
  - `pages`
  - `components/ui`
  - `components/shared`
  - `components/playground`
- Add `/playground` route and baseline interactive UI component.
- Integrate shadcn/vue foundations (`components.json`, `lib/utils.ts`, UI primitive seed).
- Add minimal unit test and Playwright smoke test.
- Generate `docs/generated/ui-inventory.md`.

## Assumptions

- Tailwind-based styling is acceptable for shadcn/vue integration baseline.
- Foundation stage should avoid business workflows and use neutral demo content only.
- Playwright uses local Vite preview server in CI.

## Verification

```bash
cd frontend
npm install
npm run lint
npm run typecheck
npm run test
npm run build
npm run test:e2e
npm run generate:ui-inventory
```
