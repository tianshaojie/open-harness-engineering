from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SysRoleBase(BaseModel):
    """角色基础模型"""

    name: str = Field(..., description="角色名称")
    org_id: int = Field(..., description="所属组织ID")
    role_type: str = Field("normal", description="角色类型")


class SysRoleCreate(SysRoleBase):
    """创建角色请求"""

    pass


class SysRoleUpdate(BaseModel):
    """更新角色请求"""

    id: int = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    status: int = Field(..., description="状态")
    role_type: Optional[str] = Field(None, description="角色类型")


class SysRoleResponse(SysRoleBase):
    """角色响应"""

    id: int = Field(..., description="角色ID")
    role_key: str = Field(..., description="角色标识")
    status: int = Field(..., description="状态")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class SysRoleListRequest(BaseModel):
    """角色列表请求"""

    org_id: int = Field(..., description="组织ID")
    name: Optional[str] = Field(None, description="角色名称搜索")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(20, ge=1, le=100, description="每页数量")


class SysRoleAssignResourcesRequest(BaseModel):
    """分配资源请求"""

    role_id: int = Field(..., description="角色ID")
    resource_ids: list[int] = Field(..., description="资源ID列表")
