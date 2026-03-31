from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

REQUIRED_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "PLANS.md",
    "AGENTS.md",
    "backend/AGENTS.md",
    "frontend/AGENTS.md",
    "docs/generated/db-schema.md",
    "docs/generated/ui-inventory.md",
]

BACKEND_COMMANDS = [
    "ruff format --check .",
    "ruff check .",
    "mypy app",
    "pytest -q",
    "alembic upgrade head",
]

FRONTEND_COMMANDS = [
    "npm run lint",
    "npm run typecheck",
    "npm run test",
    "npm run build",
    "npm run test:e2e",
]


def fail(message: str) -> None:
    print(f"[docs-guard] {message}")


def find_markdown_files() -> list[Path]:
    files = [REPO_ROOT / "README.md", REPO_ROOT / "ARCHITECTURE.md", REPO_ROOT / "PLANS.md"]
    docs_dir = REPO_ROOT / "docs"
    if docs_dir.exists():
        files.extend(sorted(docs_dir.rglob("*.md")))
    return files


def check_required_files() -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        file_path = REPO_ROOT / relative_path
        if not file_path.exists():
            errors.append(f"required file is missing: {relative_path}")
    return errors


def normalize_local_target(raw_target: str, source_file: Path) -> Path | None:
    if raw_target.startswith(("http://", "https://", "mailto:", "#")):
        return None

    without_anchor = raw_target.split("#", maxsplit=1)[0]
    if not without_anchor:
        return None

    target_path = (source_file.parent / without_anchor).resolve()
    return target_path


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for markdown_file in find_markdown_files():
        content = markdown_file.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            normalized = normalize_local_target(target, markdown_file)
            if normalized is None:
                continue
            if not normalized.exists():
                relative_source = markdown_file.relative_to(REPO_ROOT)
                errors.append(
                    f"broken local link in {relative_source}: {target} -> {normalized.relative_to(REPO_ROOT)}"
                )
    return errors


def assert_commands_present(content: str, commands: list[str], source: str) -> list[str]:
    errors: list[str] = []
    for command in commands:
        if command not in content:
            errors.append(f"missing command '{command}' in {source}")
    return errors


def check_command_consistency() -> list[str]:
    errors: list[str] = []

    readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    backend_agents = (REPO_ROOT / "backend" / "AGENTS.md").read_text(encoding="utf-8")
    frontend_agents = (REPO_ROOT / "frontend" / "AGENTS.md").read_text(encoding="utf-8")

    errors.extend(assert_commands_present(readme_text, BACKEND_COMMANDS, "README.md backend section"))
    errors.extend(assert_commands_present(backend_agents, BACKEND_COMMANDS, "backend/AGENTS.md"))

    errors.extend(assert_commands_present(readme_text, FRONTEND_COMMANDS, "README.md frontend section"))
    errors.extend(assert_commands_present(frontend_agents, FRONTEND_COMMANDS, "frontend/AGENTS.md"))

    if "python scripts/docs_guard.py" not in readme_text:
        errors.append("missing docs guard command in README.md")

    return errors


def check_plan_references() -> list[str]:
    plans_text = (REPO_ROOT / "PLANS.md").read_text(encoding="utf-8")
    expected = [
        "docs/exec-plans/active/phase-1-repo-bootstrap.md",
        "docs/exec-plans/active/phase-2-backend-foundation.md",
        "docs/exec-plans/active/phase-3-frontend-foundation.md",
        "docs/exec-plans/active/phase-4-infra-cicd.md",
        "docs/exec-plans/active/phase-5-self-review.md",
    ]

    errors: list[str] = []
    for path in expected:
        if path not in plans_text:
            errors.append(f"PLANS.md missing reference: {path}")
        if not (REPO_ROOT / path).exists():
            errors.append(f"referenced plan does not exist: {path}")

    return errors


def main() -> int:
    checks = [
        check_required_files,
        check_markdown_links,
        check_command_consistency,
        check_plan_references,
    ]

    errors: list[str] = []
    for check in checks:
        errors.extend(check())

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("[docs-guard] all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
