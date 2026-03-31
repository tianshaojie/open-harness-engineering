from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_department import SysDepartment
from app.models.sys_organization import SysOrganization
from app.repositories.sys_organization_repository import SysOrganizationRepository
from app.schemas.sys_organization import (
    SysOrganizationCreate,
    SysOrganizationUpdate,
    SysOrganizationResponse,
    SysOrganizationListRequest,
    SysDepartmentCreate,
    SysDepartmentUpdate,
    SysDepartmentResponse,
)
from app.schemas.common import PageResponse, DataResponse


class SysOrganizationService:
    """组织服务"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.org_repo = SysOrganizationRepository(session)

    async def create_organization(
        self, request: SysOrganizationCreate
    ) -> DataResponse[SysOrganizationResponse]:
        """创建组织"""
        # 检查组织编码是否已存在
        existing = await self.org_repo.get_by_code(request.org_code)
        if existing:
            raise ValueError("组织编码已存在")

        # 创建组织
        org = SysOrganization(
            name=request.name, org_code=request.org_code, org_type=request.org_type, status=1
        )
        org = await self.org_repo.create(org)
        await self.session.commit()

        return DataResponse(
            success=True, message="创建成功", data=SysOrganizationResponse.model_validate(org)
        )

    async def update_organization(self, request: SysOrganizationUpdate) -> bool:
        """更新组织"""
        update_data = {
            "name": request.name,
            "org_type": request.org_type,
            "status": request.status,
        }
        success = await self.org_repo.update_org(request.id, **update_data)
        await self.session.commit()
        return success

    async def delete_organization(self, org_id: int) -> bool:
        """删除组织"""
        success = await self.org_repo.delete_org(org_id)
        await self.session.commit()
        return success

    async def get_organization_list(
        self, request: SysOrganizationListRequest
    ) -> PageResponse[SysOrganizationResponse]:
        """获取组织列表"""
        offset = (request.page - 1) * request.size
        orgs = await self.org_repo.list_all(offset=offset, limit=request.size, name=request.name)
        total = await self.org_repo.count_all(name=request.name)

        return PageResponse(
            success=True,
            message="",
            data=[SysOrganizationResponse.model_validate(o) for o in orgs],
            total=total,
            page=request.page,
            size=request.size,
        )

    async def get_department_list(self, org_id: int) -> DataResponse[list[SysDepartmentResponse]]:
        """获取部门列表"""
        result = await self.session.execute(
            select(SysDepartment).where(SysDepartment.org_id == org_id).order_by(SysDepartment.sort)
        )
        depts = list(result.scalars().all())

        return DataResponse(
            success=True,
            message="",
            data=[SysDepartmentResponse.model_validate(d) for d in depts],
        )

    async def create_department(self, request: SysDepartmentCreate) -> SysDepartmentResponse:
        """创建部门"""
        dept = SysDepartment(
            org_id=request.org_id,
            parent_id=request.parent_id,
            dept_name=request.dept_name,
            sort=request.sort,
        )
        self.session.add(dept)
        await self.session.flush()
        await self.session.refresh(dept)
        await self.session.commit()

        return SysDepartmentResponse.model_validate(dept)

    async def update_department(self, request: SysDepartmentUpdate) -> bool:
        """更新部门"""
        from sqlalchemy import update

        stmt = (
            update(SysDepartment)
            .where(SysDepartment.id == request.id)
            .values(
                dept_name=request.dept_name, parent_id=request.parent_id, sort=request.sort
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def delete_department(self, dept_id: int) -> bool:
        """删除部门"""
        from sqlalchemy import delete

        stmt = delete(SysDepartment).where(SysDepartment.id == dept_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
