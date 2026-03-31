from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.common import CommonResponse, DataResponse, PageResponse
from app.schemas.sys_resource import (
    SysResourceCreate,
    SysResourceUpdate,
    SysResourceResponse,
    SysResourceListRequest,
)
from app.services.sys_resource_service import SysResourceService

router = APIRouter(prefix="/api/sys/resource", tags=["sys-resource"])


@router.post("/list", response_model=PageResponse[SysResourceResponse])
async def list_resources(
    request: SysResourceListRequest, db: AsyncSession = Depends(get_db)
) -> PageResponse[SysResourceResponse]:
    """获取资源列表"""
    service = SysResourceService(db)
    return await service.get_resource_list(request)


@router.post("/menu-list", response_model=DataResponse[list[SysResourceResponse]])
async def get_menu_list(db: AsyncSession = Depends(get_db)) -> DataResponse[list[SysResourceResponse]]:
    """获取菜单树"""
    service = SysResourceService(db)
    return await service.get_menu_tree()


@router.post("/create", response_model=DataResponse[SysResourceResponse])
async def create_resource(
    request: SysResourceCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[SysResourceResponse]:
    """创建资源"""
    service = SysResourceService(db)
    resource = await service.create_resource(request)
    return DataResponse(success=True, message="创建成功", data=resource)


@router.post("/update", response_model=CommonResponse)
async def update_resource(
    request: SysResourceUpdate, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """更新资源"""
    service = SysResourceService(db)
    success = await service.update_resource(request)
    if not success:
        raise HTTPException(status_code=404, detail="资源不存在")
    return CommonResponse(success=True, message="更新成功")


@router.post("/delete", response_model=CommonResponse)
async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db)) -> CommonResponse:
    """删除资源"""
    service = SysResourceService(db)
    success = await service.delete_resource(resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="资源不存在")
    return CommonResponse(success=True, message="删除成功")
