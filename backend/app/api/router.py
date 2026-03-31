from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.sys_auth import router as sys_auth_router
from app.api.routes.sys_user import router as sys_user_router
from app.api.routes.sys_organization import router as sys_organization_router
from app.api.routes.sys_role import router as sys_role_router
from app.api.routes.sys_resource import router as sys_resource_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(sys_auth_router)
api_router.include_router(sys_user_router)
api_router.include_router(sys_organization_router)
api_router.include_router(sys_role_router)
api_router.include_router(sys_resource_router)
