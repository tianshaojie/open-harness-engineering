# RBAC系统快速开始指南

## 概述

open-harness-engineering现已集成完整的RBAC（基于角色的访问控制）系统，包括：
- 用户管理
- 角色管理
- 组织架构管理
- 资源权限管理
- 动态菜单系统

## 快速开始

### 1. 安装依赖

#### 后端依赖

```bash
cd backend

# 安装基础依赖
pip install -e ".[dev]"

# 安装异步数据库驱动（根据数据库类型选择）
pip install aiosqlite      # SQLite
# 或
pip install asyncpg        # PostgreSQL
```

#### 前端依赖

```bash
cd frontend
npm install
```

### 2. 数据库初始化

```bash
cd backend

# 运行数据库迁移
alembic upgrade head
```

这将创建以下表：
- sys_organization（组织表）
- sys_department（部门表）
- sys_user（用户表）
- sys_role（角色表）
- sys_resource（资源表）
- sys_user_role（用户角色关联表）
- sys_role_resource（角色资源关联表）
- sys_sessions（会话表）
- sys_api_key（API密钥表）

并初始化：
- 超级管理员账号：`superadmin` / `Admin@123`
- 默认菜单结构

### 3. 启动服务

#### 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看API文档

#### 启动前端

```bash
cd frontend
npm run dev
```

访问 http://localhost:5173

### 4. 登录测试

使用默认账号登录：
- 用户名：`superadmin`
- 密码：`Admin@123`

**重要**：生产环境部署后请立即修改此密码！

## API使用示例

### 登录

```bash
curl -X POST http://localhost:8000/api/sys/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "superadmin",
    "password": "Admin@123"
  }'
```

响应：
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "token": "...",
    "user_id": 10000,
    "username": "superadmin",
    "org_id": 0,
    "real_name": "Super Admin"
  }
}
```

### 获取用户列表

```bash
curl -X POST http://localhost:8000/api/sys/user/list \
  -H "Content-Type: application/json" \
  -d '{
    "org_id": 1,
    "page": 1,
    "size": 20
  }'
```

### 创建组织

```bash
curl -X POST http://localhost:8000/api/sys/organization/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试公司",
    "org_code": "TEST001",
    "org_type": "COMPANY"
  }'
```

### 获取菜单树

```bash
curl -X POST http://localhost:8000/api/sys/resource/menu-list \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 前端组件使用

### DataTable组件

```vue
<template>
  <DataTable
    :search-fields="searchFields"
    :columns="columns"
    :data="users"
    :loading="loading"
    :pagination="pagination"
    @search="handleSearch"
    @page-change="handlePageChange"
    @page-size-change="handlePageSizeChange"
  >
    <!-- 自定义列插槽 -->
    <template #actions="{ row }">
      <Button @click="editUser(row)">编辑</Button>
      <Button variant="destructive" @click="deleteUser(row)">删除</Button>
    </template>
  </DataTable>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DataTable from '@/components/shared/DataTable/index.vue'
import type { SearchField, Column, PaginationData } from '@/components/shared/DataTable/index.vue'

const searchFields: SearchField[] = [
  { key: 'username', label: '用户名', type: 'input', placeholder: '请输入用户名' },
  { 
    key: 'status', 
    label: '状态', 
    type: 'select',
    options: [
      { label: '正常', value: 1 },
      { label: '禁用', value: -1 }
    ]
  }
]

const columns: Column[] = [
  { key: 'id', title: 'ID', width: 80 },
  { key: 'username', title: '用户名', width: 150 },
  { key: 'real_name', title: '真实姓名', width: 150 },
  { key: 'status', title: '状态', width: 100 },
  { key: 'actions', title: '操作', width: 200, slot: 'actions' }
]

const users = ref([])
const loading = ref(false)
const pagination = ref<PaginationData>({
  total: 0,
  page: 1,
  size: 20
})

const handleSearch = (params: Record<string, unknown>) => {
  console.log('搜索参数:', params)
  // 调用API获取数据
}

const handlePageChange = (page: number) => {
  pagination.value.page = page
  // 重新加载数据
}

const handlePageSizeChange = (size: number) => {
  pagination.value.size = size
  pagination.value.page = 1
  // 重新加载数据
}
</script>
```

## 数据库表结构

### sys_user（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键ID |
| org_id | int | 所属组织ID |
| dept_id | int | 所属部门ID |
| username | varchar(50) | 用户名（唯一） |
| password | varchar(255) | 密码（SHA256） |
| real_name | varchar(100) | 真实姓名 |
| status | smallint | 状态：1-正常, -1-已删除 |
| last_login | datetime | 最后登录时间 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |

### sys_role（角色表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| org_id | int | 所属组织ID |
| name | varchar(100) | 角色名称 |
| role_key | varchar(100) | 角色标识 |
| role_type | varchar(20) | 角色类型 |
| status | smallint | 状态 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |

### sys_resource（资源表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键ID |
| org_id | bigint | 所属租户（NULL表示系统预设） |
| pid | bigint | 父级ID |
| name | varchar(50) | 资源名称 |
| type | smallint | 类型：1目录, 2菜单, 3按钮, 4智能体 |
| path | varchar(255) | 前端路由地址 |
| perm_code | varchar(100) | 权限标识码 |
| icon | varchar(50) | 图标 |
| visible | smallint | 是否在菜单栏显示 |
| sort | int | 排序 |
| status | smallint | 状态 |
| create_time | datetime | 创建时间 |

## 权限控制流程

1. **用户登录** → 获取Token
2. **获取用户角色** → 查询sys_user_role
3. **获取角色权限** → 查询sys_role_resource
4. **获取资源列表** → 查询sys_resource
5. **生成动态菜单** → 根据权限过滤菜单
6. **页面权限控制** → 根据perm_code控制访问

## 开发建议

### 添加新的管理页面

1. 在`frontend/src/pages/sys/`创建新页面
2. 使用DataTable组件展示列表
3. 调用对应的API接口
4. 在sys_resource表中添加菜单配置

### 添加新的API端点

1. 在`backend/app/api/routes/`创建路由文件
2. 在`backend/app/services/`创建服务层
3. 在`backend/app/repositories/`创建数据访问层
4. 在`backend/app/api/router.py`注册路由

### 自定义权限验证

```python
from fastapi import Depends, HTTPException
from app.services.auth_service import AuthService

async def verify_permission(
    token: str,
    perm_code: str,
    db: AsyncSession = Depends(get_db)
) -> SysUser:
    auth_service = AuthService(db)
    user = await auth_service.verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="未授权")
    
    # 检查用户是否有指定权限
    # TODO: 实现权限检查逻辑
    
    return user
```

## 常见问题

### Q: 如何修改超级管理员密码？

A: 直接更新数据库：
```sql
UPDATE sys_user 
SET password = SHA2('新密码', 256) 
WHERE username = 'superadmin';
```

### Q: 如何添加新的组织？

A: 调用组织创建API：
```bash
POST /api/sys/organization/create
{
  "name": "组织名称",
  "org_code": "ORG001",
  "org_type": "COMPANY"
}
```

### Q: 如何为用户分配角色？

A: 调用角色分配API：
```bash
POST /api/sys/user/assign-roles
{
  "user_id": 1,
  "role_ids": [1, 2]
}
```

### Q: 如何添加新菜单？

A: 调用资源创建API：
```bash
POST /api/sys/resource/create
{
  "pid": 0,
  "name": "新菜单",
  "type": 2,
  "path": "/new-menu",
  "perm_code": "menu:new",
  "icon": "Menu",
  "visible": 1,
  "sort": 10
}
```

## 下一步

1. 完成前端登录页面和认证逻辑
2. 实现动态菜单系统
3. 创建组织、角色、资源管理页面
4. 添加权限验证中间件
5. 完善测试和文档

## 参考文档

- [RBAC实施总结](./RBAC_IMPLEMENTATION_SUMMARY.md)
- [迁移进度报告](./RBAC_MIGRATION_PROGRESS.md)
- [API文档](http://localhost:8000/docs)
