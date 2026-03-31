from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SysSession(Base):
    __tablename__ = "sys_sessions"
    __table_args__ = {"comment": "会话表"}

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="主键ID"
    )
    session_token: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="会话令牌"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True, comment="用户ID"
    )
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="所属机构ID")
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    expire_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True, comment="过期时间"
    )
