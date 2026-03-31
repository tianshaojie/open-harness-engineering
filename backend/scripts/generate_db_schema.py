from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.models import Base


def generate_markdown() -> str:
    generated_at = datetime.now(UTC).isoformat()
    lines = [
        "# Database Schema Inventory",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## SQLAlchemy Metadata Tables",
        "",
    ]

    tables = sorted(Base.metadata.tables.values(), key=lambda table: table.name)

    if not tables:
        lines.append("No application tables are defined yet.")
    else:
        for table in tables:
            lines.append(f"### {table.name}")
            for column in table.columns:
                lines.append(f"- `{column.name}`: `{column.type}`")
            lines.append("")

    lines.extend(
        [
            "## Alembic",
            "",
            "- Baseline migration exists for migration pipeline validation.",
            "- Domain tables are intentionally deferred until feature modules are introduced.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_path = repo_root / "docs" / "generated" / "db-schema.md"
    output_path.write_text(generate_markdown(), encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
