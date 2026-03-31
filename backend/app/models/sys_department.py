from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysDepartment(Base):
    __tablename__ = "sys_department"
    __table_args__ = {"comment": "部门表"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="所属机构ID")
    parent_id: Mapped[int] = mapped_column(
        Integer, server_default="0", index=True, comment="父部门ID，0表示顶级部门"
    )
    dept_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="部门名称")
    sort: Mapped[int] = mapped_column(Integer, server_default="0", comment="排序号")
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
