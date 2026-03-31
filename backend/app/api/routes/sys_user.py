from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.common import CommonResponse, DataResponse, PageResponse
from app.schemas.sys_user import (
    SysUserCreate,
    SysUserUpdate,
    SysUserResponse,
    SysUserListRequest,
    SysUserResetPasswordRequest,
    SysUserAssignRolesRequest,
)
from app.services.sys_user_service import SysUserService

router = APIRouter(prefix="/api/sys/user", tags=["sys-user"])


@router.post("/list", response_model=PageResponse[SysUserResponse])
async def list_users(
    request: SysUserListRequest, db: AsyncSession = Depends(get_db)
) -> PageResponse[SysUserResponse]:
    """获取用户列表"""
    service = SysUserService(db)
    return await service.get_user_list(request)


@router.post("/create", response_model=DataResponse[SysUserResponse])
async def create_user(
    request: SysUserCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[SysUserResponse]:
    """创建用户"""
    service = SysUserService(db)
    try:
        user = await service.create_user(request)
        return DataResponse(success=True, message="创建成功", data=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update", response_model=CommonResponse)
async def update_user(
    request: SysUserUpdate, user_id: int, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """更新用户"""
    service = SysUserService(db)
    success = await service.update_user(request, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return CommonResponse(success=True, message="更新成功")


@router.post("/delete", response_model=CommonResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> CommonResponse:
    """删除用户"""
    service = SysUserService(db)
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return CommonResponse(success=True, message="删除成功")


@router.post("/reset-password", response_model=CommonResponse)
async def reset_password(
    request: SysUserResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """重置密码"""
    service = SysUserService(db)
    success = await service.reset_password(request.id, request.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return CommonResponse(success=True, message="密码重置成功")


@router.post("/roles", response_model=DataResponse[list[int]])
async def get_user_roles(user_id: int, db: AsyncSession = Depends(get_db)) -> DataResponse[list[int]]:
    """获取用户角色"""
    service = SysUserService(db)
    role_ids = await service.get_user_roles(user_id)
    return DataResponse(success=True, message="", data=role_ids)


@router.post("/assign-roles", response_model=CommonResponse)
async def assign_roles(
    request: SysUserAssignRolesRequest, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """分配角色"""
    service = SysUserService(db)
    # 需要获取用户的org_id
    from app.repositories.sys_user_repository import SysUserRepository
    
    user_repo = SysUserRepository(db)
    user = await user_repo.get_by_id(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await service.assign_roles(request.user_id, user.org_id, request.role_ids)
    return CommonResponse(success=True, message="分配成功")
