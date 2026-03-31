from __future__ import annotations

from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_user import SysUser


class SysUserRepository:
    """用户数据访问层"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[SysUser]:
        """根据ID获取用户"""
        result = await self.session.execute(select(SysUser).where(SysUser.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[SysUser]:
        """根据用户名获取用户"""
        result = await self.session.execute(select(SysUser).where(SysUser.username == username))
        return result.scalar_one_or_none()

    async def list_by_org(
        self, org_id: int, offset: int = 0, limit: int = 20, username: Optional[str] = None
    ) -> list[SysUser]:
        """获取组织下的用户列表"""
        query = select(SysUser).where(SysUser.org_id == org_id, SysUser.status == 1)
        if username:
            query = query.where(SysUser.username.like(f"%{username}%"))
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_by_org(self, org_id: int, username: Optional[str] = None) -> int:
        """统计组织下的用户数量"""
        from sqlalchemy import func

        query = select(func.count(SysUser.id)).where(SysUser.org_id == org_id, SysUser.status == 1)
        if username:
            query = query.where(SysUser.username.like(f"%{username}%"))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, user: SysUser) -> SysUser:
        """创建用户"""
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, **kwargs: object) -> bool:
        """更新用户信息"""
        stmt = update(SysUser).where(SysUser.id == user_id).values(**kwargs)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_user(self, user_id: int) -> bool:
        """删除用户（软删除）"""
        stmt = update(SysUser).where(SysUser.id == user_id).values(status=-1)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
