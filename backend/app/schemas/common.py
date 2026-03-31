from __future__ import annotations

from typing import Generic, TypeVar, Optional

from pydantic import BaseModel, Field

T = TypeVar("T")


class CommonResponse(BaseModel):
    """通用响应"""

    success: bool = Field(..., description="是否成功")
    message: str = Field("", description="消息")
    code: int = Field(200, description="状态码")


class DataResponse(CommonResponse, Generic[T]):
    """数据响应"""

    data: Optional[T] = Field(None, description="数据")


class PageResponse(CommonResponse, Generic[T]):
    """分页响应"""

    data: list[T] = Field(default_factory=list, description="数据列表")
    total: int = Field(0, description="总数")
    page: int = Field(1, description="当前页")
    size: int = Field(20, description="每页数量")


class LoginRequest(BaseModel):
    """登录请求"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应"""

    token: str = Field(..., description="访问令牌")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    org_id: int = Field(..., description="组织ID")
    real_name: Optional[str] = Field(None, description="真实姓名")
