from __future__ import annotations

from sqlalchemy import BigInteger, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysRoleResource(Base):
    __tablename__ = "sys_role_resource"
    __table_args__ = (
        UniqueConstraint("role_id", "resource_id", name="uk_role_resource"),
        {"comment": "角色资源关联表"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="所属机构ID")
    role_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="角色ID")
    resource_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True, comment="资源ID"
    )
