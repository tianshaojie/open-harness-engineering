# AGENTS

Repository-level agent rules for `open_harness_engineering`.

## Core Rules

1. `docs` is the system of record; code and docs must evolve together.
2. For non-trivial work, create an execution plan in `docs/exec-plans/active/` before coding.
3. Keep backend and frontend concerns separated (`backend/`, `frontend/`) while sharing repository-level standards.
4. After each meaningful change, run relevant checks and record outcomes.
5. Never leave critical assumptions implicit; record them in plan docs or phase notes.

## Definition of Done (Per Change)

- Code is navigable for AI agents.
- Tests/checks for changed area are executed.
- Docs and commands remain consistent with implementation.
