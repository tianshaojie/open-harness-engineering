"""Create RBAC system tables.

Revision ID: 20260331_0002
Revises: 20260331_0001
Create Date: 2026-03-31 14:17:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260331_0002"
down_revision = "20260331_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 启用pgcrypto扩展以支持digest函数
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    
    # 1. sys_organization - 组织表
    op.create_table(
        "sys_organization",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("name", sa.String(100), nullable=False, comment="机构名称"),
        sa.Column("org_code", sa.String(50), nullable=False, comment="机构编码"),
        sa.Column("org_type", sa.String(20), server_default="COMPANY", comment="机构类型: PERSONAL/COMPANY"),
        sa.Column("status", sa.SmallInteger(), server_default="1", comment="状态: 1-正常, -1-已删除"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), comment="创建时间"),
        sa.Column("update_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP"), comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("org_code", name="uk_org_code"),
        comment="组织/机构表",
    )
    op.create_index("idx_org_status", "sys_organization", ["status"])

    # 2. sys_department - 部门表
    op.create_table(
        "sys_department",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("parent_id", sa.Integer(), server_default="0", comment="父部门ID，0表示顶级部门"),
        sa.Column("dept_name", sa.String(100), nullable=False, comment="部门名称"),
        sa.Column("sort", sa.Integer(), server_default="0", comment="排序号"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), comment="创建时间"),
        sa.PrimaryKeyConstraint("id"),
        comment="部门表",
    )
    op.create_index("idx_dept_org_id", "sys_department", ["org_id"])
    op.create_index("idx_dept_parent_id", "sys_department", ["parent_id"])

    # 3. sys_user - 用户表
    op.create_table(
        "sys_user",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("dept_id", sa.Integer(), nullable=True, comment="所属部门ID"),
        sa.Column("username", sa.String(50), nullable=False, comment="用户名（全局唯一）"),
        sa.Column("password", sa.String(255), nullable=False, comment="密码（SHA256加密）"),
        sa.Column("real_name", sa.String(100), nullable=True, comment="真实姓名"),
        sa.Column("status", sa.SmallInteger(), server_default="1", comment="状态: 1-正常, -1-已删除"),
        sa.Column("last_login", sa.DateTime(), nullable=True, comment="最后登录时间"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), comment="创建时间"),
        sa.Column("update_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP"), comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username", name="uk_username"),
        comment="用户表",
    )
    op.create_index("idx_user_org_id", "sys_user", ["org_id"])
    op.create_index("idx_user_dept_id", "sys_user", ["dept_id"])
    op.create_index("idx_user_status", "sys_user", ["status"])

    # 4. sys_role - 角色表
    op.create_table(
        "sys_role",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("name", sa.String(100), nullable=False, comment="角色名称"),
        sa.Column("role_key", sa.String(100), nullable=False, comment="角色标识"),
        sa.Column("role_type", sa.String(20), server_default="normal", comment="角色类型：superadmin-超级管理员, admin-组织管理员, normal-普通角色"),
        sa.Column("status", sa.SmallInteger(), server_default="1", comment="状态: 1-正常, -1-已删除"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), comment="创建时间"),
        sa.Column("update_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP"), comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        comment="角色表",
    )
    op.create_index("idx_role_org_id", "sys_role", ["org_id"])
    op.create_index("idx_role_key", "sys_role", ["role_key"])
    op.create_index("idx_role_type", "sys_role", ["role_type"])
    op.create_index("idx_role_status", "sys_role", ["status"])

    # 5. sys_resource - 资源表（菜单、按钮、智能体等）
    op.create_table(
        "sys_resource",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.BigInteger(), nullable=True, comment="所属租户(NULL表示系统预设)"),
        sa.Column("pid", sa.BigInteger(), server_default="0", nullable=False, comment="父级ID"),
        sa.Column("name", sa.String(50), nullable=False, comment="资源名称"),
        sa.Column("type", sa.SmallInteger(), nullable=False, comment="类型: 1目录, 2菜单, 3按钮, 4智能体"),
        sa.Column("path", sa.String(255), nullable=True, comment="前端路由地址"),
        sa.Column("perm_code", sa.String(100), nullable=True, comment="权限标识码"),
        sa.Column("icon", sa.String(50), nullable=True, comment="图标"),
        sa.Column("visible", sa.SmallInteger(), server_default="1", nullable=False, comment="是否在菜单栏显示"),
        sa.Column("sort", sa.Integer(), server_default="0", comment="排序"),
        sa.Column("status", sa.SmallInteger(), server_default="1", nullable=False, comment="1-正常, 0-停用, -1-删除"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False, comment="创建时间"),
        sa.PrimaryKeyConstraint("id"),
        comment="权限资源表",
    )
    op.create_index("idx_resource_org_id", "sys_resource", ["org_id"])
    op.create_index("idx_resource_pid", "sys_resource", ["pid"])

    # 6. sys_role_resource - 角色资源关联表
    op.create_table(
        "sys_role_resource",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("role_id", sa.Integer(), nullable=False, comment="角色ID"),
        sa.Column("resource_id", sa.BigInteger(), nullable=False, comment="资源ID"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "resource_id", name="uk_role_resource"),
        comment="角色资源关联表",
    )
    op.create_index("idx_rr_org_id", "sys_role_resource", ["org_id"])
    op.create_index("idx_rr_resource_id", "sys_role_resource", ["resource_id"])

    # 7. sys_user_role - 用户角色关联表
    op.create_table(
        "sys_user_role",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("user_id", sa.BigInteger(), nullable=False, comment="用户ID"),
        sa.Column("role_id", sa.Integer(), nullable=False, comment="角色ID"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "role_id", name="uk_user_role"),
        comment="用户角色关联表",
    )
    op.create_index("idx_ur_org_id", "sys_user_role", ["org_id"])
    op.create_index("idx_ur_role_id", "sys_user_role", ["role_id"])

    # 8. sys_sessions - 会话表
    op.create_table(
        "sys_sessions",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True, comment="主键ID"),
        sa.Column("session_token", sa.String(255), nullable=False, comment="会话令牌"),
        sa.Column("user_id", sa.BigInteger(), nullable=False, comment="用户ID"),
        sa.Column("org_id", sa.Integer(), nullable=False, comment="所属机构ID"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), comment="创建时间"),
        sa.Column("expire_time", sa.DateTime(), nullable=False, comment="过期时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_token", name="uk_session_token"),
        comment="会话表",
    )
    op.create_index("idx_session_user_id", "sys_sessions", ["user_id"])
    op.create_index("idx_session_org_id", "sys_sessions", ["org_id"])
    op.create_index("idx_session_expire_time", "sys_sessions", ["expire_time"])

    # 9. sys_api_key - API密钥表
    op.create_table(
        "sys_api_key",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True, comment="自增ID"),
        sa.Column("user_id", sa.BigInteger(), nullable=False, comment="用户ID（关联 sys_user.id）"),
        sa.Column("name", sa.String(128), nullable=False, comment="API密钥名称"),
        sa.Column("api_key", sa.String(48), nullable=False, comment="API密钥"),
        sa.Column("last_use_time", sa.DateTime(), nullable=True, comment="最后使用时间"),
        sa.Column("create_by", sa.BigInteger(), nullable=False, comment="创建人用户ID"),
        sa.Column("create_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False, comment="创建时间"),
        sa.Column("update_time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP"), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key", name="uk_api_key"),
        comment="API密钥表（基于sys_user）",
    )
    op.create_index("idx_apikey_user_id", "sys_api_key", ["user_id"])

    # 初始化数据：创建超级管理员
    # 使用PostgreSQL的digest函数生成SHA256哈希
    op.execute(
        """
        INSERT INTO sys_user (id, org_id, dept_id, username, password, real_name, status, create_time, update_time)
        VALUES (10000, 0, NULL, 'superadmin', encode(digest('Admin@123', 'sha256'), 'hex'), 'Super Admin', 1, NOW(), NOW())
        """
    )


def downgrade() -> None:
    # 删除表的顺序与创建相反
    op.drop_table("sys_api_key")
    op.drop_table("sys_sessions")
    op.drop_table("sys_user_role")
    op.drop_table("sys_role_resource")
    op.drop_table("sys_resource")
    op.drop_table("sys_role")
    op.drop_table("sys_user")
    op.drop_table("sys_department")
    op.drop_table("sys_organization")
