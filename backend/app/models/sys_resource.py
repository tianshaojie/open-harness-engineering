from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Integer, String, SmallInteger, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysResource(Base):
    __tablename__ = "sys_resource"
    __table_args__ = {"comment": "权限资源表"}

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="主键ID"
    )
    org_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True, index=True, comment="所属租户(NULL表示系统预设)"
    )
    pid: Mapped[int] = mapped_column(
        BigInteger, server_default="0", nullable=False, index=True, comment="父级ID"
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="资源名称")
    type: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="类型: 1目录, 2菜单, 3按钮, 4智能体"
    )
    path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="前端路由地址")
    perm_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="权限标识码")
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="图标")
    visible: Mapped[int] = mapped_column(
        SmallInteger, server_default="1", nullable=False, comment="是否在菜单栏显示"
    )
    sort: Mapped[int] = mapped_column(Integer, server_default="0", comment="排序")
    status: Mapped[int] = mapped_column(
        SmallInteger, server_default="1", nullable=False, comment="1-正常, 0-停用, -1-删除"
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False, comment="创建时间"
    )
