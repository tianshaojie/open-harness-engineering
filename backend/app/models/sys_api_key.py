from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysApiKey(Base):
    __tablename__ = "sys_api_key"
    __table_args__ = {"comment": "API密钥表（基于sys_user）"}

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="自增ID"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True, comment="用户ID（关联 sys_user.id）"
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="API密钥名称")
    api_key: Mapped[str] = mapped_column(String(48), nullable=False, unique=True, comment="API密钥")
    last_use_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="最后使用时间"
    )
    create_by: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="创建人用户ID")
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False, comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="更新时间",
    )
