from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Integer, String, SmallInteger, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysUser(Base):
    __tablename__ = "sys_user"
    __table_args__ = {"comment": "用户表"}

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="主键ID"
    )
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="所属机构ID")
    dept_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, index=True, comment="所属部门ID"
    )
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, comment="用户名（全局唯一）"
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（SHA256加密）")
    real_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="真实姓名")
    status: Mapped[int] = mapped_column(
        SmallInteger, server_default="1", index=True, comment="状态: 1-正常, -1-已删除"
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="最后登录时间"
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
