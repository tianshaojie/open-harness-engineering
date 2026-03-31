from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.common import CommonResponse, DataResponse, PageResponse
from app.schemas.sys_organization import (
    SysOrganizationCreate,
    SysOrganizationUpdate,
    SysOrganizationResponse,
    SysOrganizationListRequest,
    SysDepartmentCreate,
    SysDepartmentUpdate,
    SysDepartmentResponse,
)
from app.services.sys_organization_service import SysOrganizationService

router = APIRouter(prefix="/api/sys/org", tags=["sys-organization"])


@router.post("/list", response_model=PageResponse[SysOrganizationResponse])
async def list_organizations(
    request: SysOrganizationListRequest, db: AsyncSession = Depends(get_db)
) -> PageResponse[SysOrganizationResponse]:
    """获取组织列表"""
    service = SysOrganizationService(db)
    return await service.get_organization_list(request)


@router.post("/create", response_model=DataResponse[SysOrganizationResponse])
async def create_organization(
    request: SysOrganizationCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[SysOrganizationResponse]:
    """创建组织"""
    service = SysOrganizationService(db)
    try:
        return await service.create_organization(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update", response_model=CommonResponse)
async def update_organization(
    request: SysOrganizationUpdate, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """更新组织"""
    service = SysOrganizationService(db)
    success = await service.update_organization(request)
    if not success:
        raise HTTPException(status_code=404, detail="组织不存在")
    return CommonResponse(success=True, message="更新成功")


@router.post("/delete", response_model=CommonResponse)
async def delete_organization(org_id: int, db: AsyncSession = Depends(get_db)) -> CommonResponse:
    """删除组织"""
    service = SysOrganizationService(db)
    success = await service.delete_organization(org_id)
    if not success:
        raise HTTPException(status_code=404, detail="组织不存在")
    return CommonResponse(success=True, message="删除成功")


# 部门相关接口
@router.post("/dept/list", response_model=DataResponse[list[SysDepartmentResponse]])
async def list_departments(
    org_id: int, db: AsyncSession = Depends(get_db)
) -> DataResponse[list[SysDepartmentResponse]]:
    """获取部门列表"""
    service = SysOrganizationService(db)
    return await service.get_department_list(org_id)


@router.post("/dept/create", response_model=DataResponse[SysDepartmentResponse])
async def create_department(
    request: SysDepartmentCreate, db: AsyncSession = Depends(get_db)
) -> DataResponse[SysDepartmentResponse]:
    """创建部门"""
    service = SysOrganizationService(db)
    dept = await service.create_department(request)
    return DataResponse(success=True, message="创建成功", data=dept)


@router.post("/dept/update", response_model=CommonResponse)
async def update_department(
    request: SysDepartmentUpdate, db: AsyncSession = Depends(get_db)
) -> CommonResponse:
    """更新部门"""
    service = SysOrganizationService(db)
    success = await service.update_department(request)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return CommonResponse(success=True, message="更新成功")


@router.post("/dept/delete", response_model=CommonResponse)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)) -> CommonResponse:
    """删除部门"""
    service = SysOrganizationService(db)
    success = await service.delete_department(dept_id)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return CommonResponse(success=True, message="删除成功")
