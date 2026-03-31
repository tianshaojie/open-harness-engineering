from __future__ import annotations

from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_role import SysRole
from app.models.sys_role_resource import SysRoleResource


class SysRoleRepository:
    """角色数据访问层"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, role_id: int) -> Optional[SysRole]:
        """根据ID获取角色"""
        result = await self.session.execute(select(SysRole).where(SysRole.id == role_id))
        return result.scalar_one_or_none()

    async def list_by_org(
        self, org_id: int, offset: int = 0, limit: int = 20, name: Optional[str] = None
    ) -> list[SysRole]:
        """获取组织下的角色列表"""
        query = select(SysRole).where(SysRole.org_id == org_id, SysRole.status == 1)
        if name:
            query = query.where(SysRole.name.like(f"%{name}%"))
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_by_org(self, org_id: int, name: Optional[str] = None) -> int:
        """统计组织下的角色数量"""
        from sqlalchemy import func

        query = select(func.count(SysRole.id)).where(SysRole.org_id == org_id, SysRole.status == 1)
        if name:
            query = query.where(SysRole.name.like(f"%{name}%"))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, role: SysRole) -> SysRole:
        """创建角色"""
        self.session.add(role)
        await self.session.flush()
        await self.session.refresh(role)
        return role

    async def update_role(self, role_id: int, **kwargs: object) -> bool:
        """更新角色信息"""
        stmt = update(SysRole).where(SysRole.id == role_id).values(**kwargs)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_role(self, role_id: int) -> bool:
        """删除角色（软删除）"""
        stmt = update(SysRole).where(SysRole.id == role_id).values(status=-1)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def get_role_resources(self, role_id: int) -> list[int]:
        """获取角色的资源ID列表"""
        result = await self.session.execute(
            select(SysRoleResource.resource_id).where(SysRoleResource.role_id == role_id)
        )
        return list(result.scalars().all())

    async def assign_resources(self, role_id: int, org_id: int, resource_ids: list[int]) -> None:
        """分配资源给角色"""
        # 先删除旧的关联
        await self.session.execute(
            delete(SysRoleResource).where(SysRoleResource.role_id == role_id)
        )
        # 添加新的关联
        for resource_id in resource_ids:
            role_resource = SysRoleResource(
                org_id=org_id, role_id=role_id, resource_id=resource_id
            )
            self.session.add(role_resource)
