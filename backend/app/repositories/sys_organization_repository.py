from __future__ import annotations

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_organization import SysOrganization


class SysOrganizationRepository:
    """组织数据访问层"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, org_id: int) -> Optional[SysOrganization]:
        """根据ID获取组织"""
        result = await self.session.execute(
            select(SysOrganization).where(SysOrganization.id == org_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, org_code: str) -> Optional[SysOrganization]:
        """根据组织编码获取组织"""
        result = await self.session.execute(
            select(SysOrganization).where(SysOrganization.org_code == org_code)
        )
        return result.scalar_one_or_none()

    async def list_all(
        self, offset: int = 0, limit: int = 20, name: Optional[str] = None
    ) -> list[SysOrganization]:
        """获取组织列表"""
        query = select(SysOrganization).where(SysOrganization.status == 1)
        if name:
            query = query.where(SysOrganization.name.like(f"%{name}%"))
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_all(self, name: Optional[str] = None) -> int:
        """统计组织数量"""
        from sqlalchemy import func

        query = select(func.count(SysOrganization.id)).where(SysOrganization.status == 1)
        if name:
            query = query.where(SysOrganization.name.like(f"%{name}%"))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, org: SysOrganization) -> SysOrganization:
        """创建组织"""
        self.session.add(org)
        await self.session.flush()
        await self.session.refresh(org)
        return org

    async def update_org(self, org_id: int, **kwargs: object) -> bool:
        """更新组织信息"""
        stmt = update(SysOrganization).where(SysOrganization.id == org_id).values(**kwargs)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_org(self, org_id: int) -> bool:
        """删除组织（软删除）"""
        stmt = update(SysOrganization).where(SysOrganization.id == org_id).values(status=-1)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
