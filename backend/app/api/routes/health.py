from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.schemas.health import HealthResponse, ReadyResponse
from app.services.health_service import get_readiness_report

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadyResponse)
def ready(response: Response) -> ReadyResponse:
    readiness = get_readiness_report()
    if readiness.status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return readiness
