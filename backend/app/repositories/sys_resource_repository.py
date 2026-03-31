from __future__ import annotations

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_resource import SysResource


class SysResourceRepository:
    """资源数据访问层"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, resource_id: int) -> Optional[SysResource]:
        """根据ID获取资源"""
        result = await self.session.execute(
            select(SysResource).where(SysResource.id == resource_id)
        )
        return result.scalar_one_or_none()

    async def list_all(
        self, offset: int = 0, limit: int = 100, name: Optional[str] = None
    ) -> list[SysResource]:
        """获取资源列表"""
        query = select(SysResource).where(SysResource.status == 1)
        if name:
            query = query.where(SysResource.name.like(f"%{name}%"))
        query = query.order_by(SysResource.sort).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_menu_tree(self) -> list[SysResource]:
        """获取菜单树（目录和菜单）"""
        result = await self.session.execute(
            select(SysResource)
            .where(SysResource.status == 1, SysResource.type.in_([1, 2]))
            .order_by(SysResource.sort)
        )
        return list(result.scalars().all())

    async def create(self, resource: SysResource) -> SysResource:
        """创建资源"""
        self.session.add(resource)
        await self.session.flush()
        await self.session.refresh(resource)
        return resource

    async def update_resource(self, resource_id: int, **kwargs: object) -> bool:
        """更新资源信息"""
        stmt = update(SysResource).where(SysResource.id == resource_id).values(**kwargs)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_resource(self, resource_id: int) -> bool:
        """删除资源（软删除）"""
        stmt = update(SysResource).where(SysResource.id == resource_id).values(status=-1)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
