from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_role import SysRole
from app.repositories.sys_role_repository import SysRoleRepository
from app.schemas.sys_role import (
    SysRoleCreate,
    SysRoleUpdate,
    SysRoleResponse,
    SysRoleListRequest,
)
from app.schemas.common import PageResponse, DataResponse


class SysRoleService:
    """角色服务"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.role_repo = SysRoleRepository(session)

    async def create_role(self, request: SysRoleCreate) -> SysRoleResponse:
        """创建角色"""
        # 生成角色标识
        role_key = f"role_{request.name}_{request.org_id}"

        role = SysRole(
            name=request.name,
            org_id=request.org_id,
            role_key=role_key,
            role_type=request.role_type,
            status=1,
        )
        role = await self.role_repo.create(role)
        await self.session.commit()

        return SysRoleResponse.model_validate(role)

    async def update_role(self, request: SysRoleUpdate) -> bool:
        """更新角色"""
        update_data = request.model_dump(exclude={"id"}, exclude_unset=True)
        success = await self.role_repo.update_role(request.id, **update_data)
        await self.session.commit()
        return success

    async def delete_role(self, role_id: int) -> bool:
        """删除角色"""
        success = await self.role_repo.delete_role(role_id)
        await self.session.commit()
        return success

    async def get_role_list(self, request: SysRoleListRequest) -> PageResponse[SysRoleResponse]:
        """获取角色列表"""
        offset = (request.page - 1) * request.size
        roles = await self.role_repo.list_by_org(
            request.org_id, offset=offset, limit=request.size, name=request.name
        )
        total = await self.role_repo.count_by_org(request.org_id, name=request.name)

        return PageResponse(
            success=True,
            message="",
            data=[SysRoleResponse.model_validate(r) for r in roles],
            total=total,
            page=request.page,
            size=request.size,
        )

    async def get_role_resources(self, role_id: int) -> DataResponse[list[int]]:
        """获取角色的资源ID列表"""
        resource_ids = await self.role_repo.get_role_resources(role_id)
        return DataResponse(success=True, message="", data=resource_ids)

    async def assign_resources(self, role_id: int, org_id: int, resource_ids: list[int]) -> None:
        """分配资源给角色"""
        await self.role_repo.assign_resources(role_id, org_id, resource_ids)
        await self.session.commit()
