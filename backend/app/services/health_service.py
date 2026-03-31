from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_engine
from app.schemas.health import ReadyResponse

logger = logging.getLogger(__name__)


def get_readiness_report() -> ReadyResponse:
    try:
        engine = get_engine()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return ReadyResponse(status="ready", detail="database-reachable")
    except SQLAlchemyError as exc:
        logger.warning(
            "readiness_check_failed",
            extra={"error": str(exc)},
        )
        return ReadyResponse(status="not_ready", detail="database-unreachable")
