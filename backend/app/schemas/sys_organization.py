from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SysOrganizationBase(BaseModel):
    """组织基础模型"""

    name: str = Field(..., description="组织名称")
    org_code: str = Field(..., description="组织编码")
    org_type: str = Field("COMPANY", description="组织类型")


class SysOrganizationCreate(SysOrganizationBase):
    """创建组织请求"""

    pass


class SysOrganizationUpdate(BaseModel):
    """更新组织请求"""

    id: int = Field(..., description="组织ID")
    name: str = Field(..., description="组织名称")
    org_type: str = Field(..., description="组织类型")
    status: int = Field(..., description="状态")


class SysOrganizationResponse(SysOrganizationBase):
    """组织响应"""

    id: int = Field(..., description="组织ID")
    status: int = Field(..., description="状态")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class SysOrganizationListRequest(BaseModel):
    """组织列表请求"""

    name: Optional[str] = Field(None, description="组织名称搜索")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(20, ge=1, le=100, description="每页数量")


class SysDepartmentBase(BaseModel):
    """部门基础模型"""

    org_id: int = Field(..., description="所属组织ID")
    parent_id: int = Field(0, description="父部门ID")
    dept_name: str = Field(..., description="部门名称")
    sort: int = Field(0, description="排序号")


class SysDepartmentCreate(SysDepartmentBase):
    """创建部门请求"""

    pass


class SysDepartmentUpdate(BaseModel):
    """更新部门请求"""

    id: int = Field(..., description="部门ID")
    dept_name: str = Field(..., description="部门名称")
    parent_id: int = Field(..., description="父部门ID")
    sort: int = Field(..., description="排序号")


class SysDepartmentResponse(SysDepartmentBase):
    """部门响应"""

    id: int = Field(..., description="部门ID")
    create_time: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
