"""Initialize default menu and resource data.

Revision ID: 20260331_0003
Revises: 20260331_0002
Create Date: 2026-03-31 14:18:00
"""

from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260331_0003"
down_revision = "20260331_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 插入默认菜单结构 - 使用PostgreSQL的WITH RETURNING语法
    op.execute(
        """
        -- 主页分组
        WITH home_group AS (
            INSERT INTO sys_resource (org_id, pid, name, type, path, perm_code, icon, visible, sort, status)
            VALUES (NULL::bigint, 0, '主页', 1, NULL, NULL, 'Home', 1, 1, 1)
            RETURNING id
        )
        INSERT INTO sys_resource (org_id, pid, name, type, path, perm_code, icon, visible, sort, status)
        SELECT NULL::bigint, id, '概览', 2, '/home/overview', 'menu:overview', 'Home', 1, 1, 1
        FROM home_group;
        """
    )
    
    op.execute(
        """
        -- 系统管理分组
        WITH sys_group AS (
            INSERT INTO sys_resource (org_id, pid, name, type, path, perm_code, icon, visible, sort, status)
            VALUES (NULL::bigint, 0, '系统管理', 1, NULL, NULL, 'Settings', 1, 20, 1)
            RETURNING id
        )
        INSERT INTO sys_resource (org_id, pid, name, type, path, perm_code, icon, visible, sort, status)
        SELECT NULL::bigint, id, '组织与成员', 2, '/sys/organization', 'menu:sys_org', 'Building2', 1, 21, 1
        FROM sys_group
        UNION ALL
        SELECT NULL::bigint, id, '角色管理', 2, '/sys/role', 'menu:sys_role', 'ShieldCheck', 1, 22, 1
        FROM sys_group
        UNION ALL
        SELECT NULL::bigint, id, '资源管理', 2, '/sys/resource', 'menu:sys_resource', 'Lock', 1, 23, 1
        FROM sys_group;
        """
    )


def downgrade() -> None:
    # 删除初始化的菜单数据
    op.execute("DELETE FROM sys_resource WHERE org_id IS NULL")
