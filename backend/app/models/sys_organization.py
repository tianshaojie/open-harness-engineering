from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, SmallInteger, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysOrganization(Base):
    __tablename__ = "sys_organization"
    __table_args__ = {"comment": "组织/机构表"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="机构名称")
    org_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="机构编码")
    org_type: Mapped[str] = mapped_column(
        String(20), server_default="COMPANY", comment="机构类型: PERSONAL/COMPANY"
    )
    status: Mapped[int] = mapped_column(
        SmallInteger, server_default="1", comment="状态: 1-正常, -1-已删除"
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
