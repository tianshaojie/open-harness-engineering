from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_session import SysSession
from app.models.sys_user import SysUser
from app.repositories.sys_user_repository import SysUserRepository
from app.schemas.common import LoginRequest, LoginResponse


class AuthService:
    """认证服务"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = SysUserRepository(session)

    @staticmethod
    def hash_password(password: str) -> str:
        """SHA256加密密码"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_token() -> str:
        """生成会话令牌"""
        return secrets.token_urlsafe(32)

    async def login(self, request: LoginRequest) -> Optional[LoginResponse]:
        """用户登录"""
        print(f"\n=== 登录请求 ===")
        print(f"用户名: {request.username}")
        print(f"密码: {request.password}")
        
        # 查找用户
        user = await self.user_repo.get_by_username(request.username)
        print(f"找到用户: {user is not None}")
        if user:
            print(f"用户状态: {user.status}")
            print(f"数据库密码: {user.password}")
        
        if not user or user.status != 1:
            print("用户不存在或状态异常")
            return None

        # 验证密码
        hashed_password = self.hash_password(request.password)
        print(f"输入密码哈希: {hashed_password}")
        print(f"密码匹配: {user.password == hashed_password}")
        
        if user.password != hashed_password:
            print("密码不匹配")
            return None

        # 生成会话令牌
        token = self.generate_token()
        expire_time = datetime.now() + timedelta(days=7)

        # 创建会话
        session = SysSession(
            session_token=token,
            user_id=user.id,
            org_id=user.org_id,
            expire_time=expire_time,
        )
        self.session.add(session)

        # 更新最后登录时间
        await self.user_repo.update_user(user.id, last_login=datetime.now())

        await self.session.commit()

        return LoginResponse(
            token=token,
            user_id=user.id,
            username=user.username,
            org_id=user.org_id,
            real_name=user.real_name,
        )

    async def verify_token(self, token: str) -> Optional[SysUser]:
        """验证令牌并返回用户"""
        from sqlalchemy import select

        # 查找会话
        result = await self.session.execute(
            select(SysSession).where(
                SysSession.session_token == token, SysSession.expire_time > datetime.now()
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            return None

        # 返回用户
        return await self.user_repo.get_by_id(session.user_id)
