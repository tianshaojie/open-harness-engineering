from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SysResourceBase(BaseModel):
    """资源基础模型"""

    name: str = Field(..., description="资源名称")
    type: int = Field(..., description="类型: 1目录, 2菜单, 3按钮, 4智能体")
    pid: int = Field(0, description="父级ID")
    path: Optional[str] = Field(None, description="前端路由地址")
    perm_code: Optional[str] = Field(None, description="权限标识码")
    icon: Optional[str] = Field(None, description="图标")
    visible: int = Field(1, description="是否在菜单栏显示")
    sort: int = Field(0, description="排序")


class SysResourceCreate(SysResourceBase):
    """创建资源请求"""

    pass


class SysResourceUpdate(BaseModel):
    """更新资源请求"""

    id: int = Field(..., description="资源ID")
    name: str = Field(..., description="资源名称")
    type: int = Field(..., description="类型")
    pid: int = Field(..., description="父级ID")
    path: Optional[str] = Field(None, description="前端路由地址")
    perm_code: Optional[str] = Field(None, description="权限标识码")
    icon: Optional[str] = Field(None, description="图标")
    visible: int = Field(..., description="是否在菜单栏显示")
    sort: int = Field(..., description="排序")


class SysResourceResponse(SysResourceBase):
    """资源响应"""

    id: int = Field(..., description="资源ID")
    org_id: Optional[int] = Field(None, description="所属租户")
    status: int = Field(..., description="状态")
    create_time: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class SysResourceListRequest(BaseModel):
    """资源列表请求"""

    name: Optional[str] = Field(None, description="资源名称搜索")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(100, ge=1, le=200, description="每页数量")
