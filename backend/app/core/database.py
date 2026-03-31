from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_ENGINE: Engine | None = None
_SESSION_FACTORY: sessionmaker[Session] | None = None


def _build_engine(database_url: str) -> Engine:
    connect_args: dict[str, bool] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def reset_engine(database_url: str | None = None) -> None:
    global _ENGINE, _SESSION_FACTORY

    if _ENGINE is not None:
        _ENGINE.dispose()

    resolved_url = database_url or get_settings().database_url
    _ENGINE = _build_engine(resolved_url)
    _SESSION_FACTORY = sessionmaker(bind=_ENGINE, autoflush=False, autocommit=False)


def get_engine() -> Engine:
    global _ENGINE

    if _ENGINE is None:
        reset_engine()

    assert _ENGINE is not None
    return _ENGINE


def get_db() -> Generator[Session, None, None]:
    global _SESSION_FACTORY

    if _SESSION_FACTORY is None:
        reset_engine()

    assert _SESSION_FACTORY is not None
    db = _SESSION_FACTORY()
    try:
        yield db
    finally:
        db.close()
