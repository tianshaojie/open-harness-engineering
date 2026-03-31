from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.common import CommonResponse, DataResponse, PageResponse
from app.schemas.sys_role import (
    SysRoleCreate,
    SysRoleUpdate,
    SysRoleResponse,
    SysRoleListRequest,
    SysRoleAssignResourcesRequest,
)
from app.services.sys_role_service import SysRoleService

router = APIRouter(prefix="/api/sys/role", tags=["sys-role"])


@router.post("/list", response_model=PageResponse[SysRoleResponse])
async def list_roles(
    request: SysRoleListRequest, db: AsyncSession = Depends(get_db)
) -> PageResponse[SysRoleResponse]:
    """获取角色列表"""
    service = SysRoleService(db)
    return await service.get_role_list(request)


@router.post("/create", response_model=DataResponse[SysRoleResponse])
async def create_role(
    request: SysRoleCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[SysRoleResponse]:
    """创建角色"""
    service = SysRoleService(db)
    role = await service.create_role(request)
    return DataResponse(success=True, message="创建成功", data=role)


@router.post("/update", response_model=CommonResponse)
async def update_role(
    request: SysRoleUpdate, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """更新角色"""
    service = SysRoleService(db)
    success = await service.update_role(request)
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    return CommonResponse(success=True, message="更新成功")


@router.post("/delete", response_model=CommonResponse)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)) -> CommonResponse:
    """删除角色"""
    service = SysRoleService(db)
    success = await service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    return CommonResponse(success=True, message="删除成功")


@router.post("/resources", response_model=DataResponse[list[int]])
async def get_role_resources(
    role_id: int, db: AsyncSession = Depends(get_db)
) -> DataResponse[list[int]]:
    """获取角色资源"""
    service = SysRoleService(db)
    return await service.get_role_resources(role_id)


@router.post("/assign-resources", response_model=CommonResponse)
async def assign_resources(
    request: SysRoleAssignResourcesRequest, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """分配资源"""
    service = SysRoleService(db)
    # 需要获取角色的org_id
    from app.repositories.sys_role_repository import SysRoleRepository
    
    role_repo = SysRoleRepository(db)
    role = await role_repo.get_by_id(request.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    await service.assign_resources(request.role_id, role.org_id, request.resource_ids)
    return CommonResponse(success=True, message="分配成功")
