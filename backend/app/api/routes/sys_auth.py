from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.common import LoginRequest, DataResponse, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/sys", tags=["sys-auth"])


@router.post("/login", response_model=DataResponse[LoginResponse])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)) -> DataResponse[LoginResponse]:
    """用户登录"""
    auth_service = AuthService(db)
    result = await auth_service.login(request)
    
    if not result:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    return DataResponse(success=True, message="登录成功", data=result)
