from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SysUserBase(BaseModel):
    """用户基础模型"""

    username: str = Field(..., description="用户名")
    real_name: Optional[str] = Field(None, description="真实姓名")
    org_id: int = Field(..., description="所属组织ID")
    dept_id: Optional[int] = Field(None, description="所属部门ID")


class SysUserCreate(SysUserBase):
    """创建用户请求"""

    password: str = Field(..., description="密码")


class SysUserUpdate(BaseModel):
    """更新用户请求"""

    real_name: Optional[str] = Field(None, description="真实姓名")
    dept_id: Optional[int] = Field(None, description="所属部门ID")
    status: Optional[int] = Field(None, description="状态")


class SysUserResponse(SysUserBase):
    """用户响应"""

    id: int = Field(..., description="用户ID")
    status: int = Field(..., description="状态")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class SysUserListRequest(BaseModel):
    """用户列表请求"""

    org_id: int = Field(..., description="组织ID")
    username: Optional[str] = Field(None, description="用户名搜索")
    real_name: Optional[str] = Field(None, description="真实姓名搜索")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(20, ge=1, le=100, description="每页数量")


class SysUserResetPasswordRequest(BaseModel):
    """重置密码请求"""

    id: int = Field(..., description="用户ID")
    new_password: str = Field(..., description="新密码")


class SysUserAssignRolesRequest(BaseModel):
    """分配角色请求"""

    user_id: int = Field(..., description="用户ID")
    role_ids: list[int] = Field(..., description="角色ID列表")
