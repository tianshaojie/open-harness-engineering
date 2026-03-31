from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_ENGINE: Engine | None = None
_SESSION_FACTORY: sessionmaker[Session] | None = None
_ASYNC_ENGINE: AsyncEngine | None = None
_ASYNC_SESSION_FACTORY: async_sessionmaker[AsyncSession] | None = None


def _build_engine(database_url: str) -> Engine:
    connect_args: dict[str, bool] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def _build_async_engine(database_url: str) -> AsyncEngine:
    # 转换同步URL为异步URL
    async_url = database_url.replace("sqlite+pysqlite://", "sqlite+aiosqlite://")
    async_url = async_url.replace("postgresql://", "postgresql+asyncpg://")
    async_url = async_url.replace("mysql://", "mysql+aiomysql://")
    
    connect_args: dict[str, bool] = {}
    if async_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_async_engine(
        async_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def reset_engine(database_url: str | None = None) -> None:
    global _ENGINE, _SESSION_FACTORY, _ASYNC_ENGINE, _ASYNC_SESSION_FACTORY

    if _ENGINE is not None:
        _ENGINE.dispose()

    resolved_url = database_url or get_settings().database_url
    _ENGINE = _build_engine(resolved_url)
    _SESSION_FACTORY = sessionmaker(bind=_ENGINE, autoflush=False, autocommit=False)
    
    # 创建异步引擎和会话工厂
    _ASYNC_ENGINE = _build_async_engine(resolved_url)
    _ASYNC_SESSION_FACTORY = async_sessionmaker(
        bind=_ASYNC_ENGINE, autoflush=False, autocommit=False, expire_on_commit=False
    )


def get_engine() -> Engine:
    global _ENGINE

    if _ENGINE is None:
        reset_engine()

    assert _ENGINE is not None
    return _ENGINE


def get_async_engine() -> AsyncEngine:
    global _ASYNC_ENGINE

    if _ASYNC_ENGINE is None:
        reset_engine()

    assert _ASYNC_ENGINE is not None
    return _ASYNC_ENGINE


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


def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    """获取异步会话工厂"""
    global _ASYNC_SESSION_FACTORY
    
    if _ASYNC_SESSION_FACTORY is None:
        reset_engine()
    
    assert _ASYNC_SESSION_FACTORY is not None
    return _ASYNC_SESSION_FACTORY
