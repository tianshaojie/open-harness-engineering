from __future__ import annotations

import hashlib
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_user import SysUser
from app.models.sys_user_role import SysUserRole
from app.repositories.sys_user_repository import SysUserRepository
from app.schemas.sys_user import (
    SysUserCreate,
    SysUserUpdate,
    SysUserResponse,
    SysUserListRequest,
)
from app.schemas.common import PageResponse


class SysUserService:
    """用户服务"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = SysUserRepository(session)

    @staticmethod
    def hash_password(password: str) -> str:
        """SHA256加密密码"""
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_user(self, request: SysUserCreate) -> SysUserResponse:
        """创建用户"""
        # 检查用户名是否已存在
        existing = await self.user_repo.get_by_username(request.username)
        if existing:
            raise ValueError("用户名已存在")

        # 创建用户
        user = SysUser(
            username=request.username,
            password=self.hash_password(request.password),
            real_name=request.real_name,
            org_id=request.org_id,
            dept_id=request.dept_id,
            status=1,
        )
        user = await self.user_repo.create(user)
        await self.session.commit()

        return SysUserResponse.model_validate(user)

    async def update_user(self, request: SysUserUpdate, user_id: int) -> bool:
        """更新用户"""
        update_data = request.model_dump(exclude_unset=True)
        success = await self.user_repo.update_user(user_id, **update_data)
        await self.session.commit()
        return success

    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        success = await self.user_repo.delete_user(user_id)
        await self.session.commit()
        return success

    async def get_user_list(self, request: SysUserListRequest) -> PageResponse[SysUserResponse]:
        """获取用户列表"""
        offset = (request.page - 1) * request.size
        users = await self.user_repo.list_by_org(
            request.org_id, offset=offset, limit=request.size, username=request.username
        )
        total = await self.user_repo.count_by_org(request.org_id, username=request.username)

        return PageResponse(
            success=True,
            message="",
            data=[SysUserResponse.model_validate(u) for u in users],
            total=total,
            page=request.page,
            size=request.size,
        )

    async def reset_password(self, user_id: int, new_password: str) -> bool:
        """重置密码"""
        hashed_password = self.hash_password(new_password)
        success = await self.user_repo.update_user(user_id, password=hashed_password)
        await self.session.commit()
        return success

    async def get_user_roles(self, user_id: int) -> list[int]:
        """获取用户的角色ID列表"""
        result = await self.session.execute(
            select(SysUserRole.role_id).where(SysUserRole.user_id == user_id)
        )
        return list(result.scalars().all())

    async def assign_roles(self, user_id: int, org_id: int, role_ids: list[int]) -> None:
        """分配角色给用户"""
        # 先删除旧的关联
        await self.session.execute(delete(SysUserRole).where(SysUserRole.user_id == user_id))

        # 添加新的关联
        for role_id in role_ids:
            user_role = SysUserRole(org_id=org_id, user_id=user_id, role_id=role_id)
            self.session.add(user_role)

        await self.session.commit()
