# Phase 5 Plan: Self Review and Docs Reconciliation

## Goal

Run a full consistency pass across naming, structure, commands, and docs so repository guidance matches executable reality.

## Scope

- Review generated code and workflow naming consistency.
- Ensure README commands run as documented.
- Ensure generated docs (`db-schema`, `ui-inventory`) are up to date.
- Ensure links and plan references are valid.
- Record residual risks explicitly.

## Assumptions

- Current repository is bootstrap stage; no business modules are expected.
- CI execution cannot be fully simulated locally (GitHub-hosted environment differences), but local command parity can be validated.

## Verification

- `python scripts/docs_guard.py`
- backend command suite
- frontend command suite
