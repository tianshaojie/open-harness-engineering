from __future__ import annotations

from collections.abc import Generator

import pytest


@pytest.fixture(autouse=True)
def configure_test_database(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine("sqlite+pysqlite:///:memory:")
    yield
