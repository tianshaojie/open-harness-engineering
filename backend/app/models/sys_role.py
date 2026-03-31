from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, SmallInteger, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysRole(Base):
    __tablename__ = "sys_role"
    __table_args__ = {"comment": "角色表"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="所属机构ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="角色名称")
    role_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="角色标识")
    role_type: Mapped[str] = mapped_column(
        String(20),
        server_default="normal",
        index=True,
        comment="角色类型：superadmin-超级管理员, admin-组织管理员, normal-普通角色",
    )
    status: Mapped[int] = mapped_column(
        SmallInteger, server_default="1", index=True, comment="状态: 1-正常, -1-已删除"
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        comment="更新时间",
    )
