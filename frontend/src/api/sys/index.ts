import { sysPost } from './http'
import {
  SYS_LOGIN_API, SYS_ORG_API, SYS_RESOURCE_API, SYS_ROLE_API, SYS_USER_API, SYS_API_KEY_API
} from './constants'
import type {
  SysLoginRequest, SysLoginResponse,
  PageResponse, DataResponse, CommonResponse,
  SysOrg, SysDept, SysResource, SysRole, SysUser, SysApiKey, OrgCreateData
} from './types'

export const sysLoginApi = {
  login: (data: SysLoginRequest) => sysPost<SysLoginResponse>(SYS_LOGIN_API.LOGIN, data),
}

export const sysOrgApi = {
  list: (data: { name?: string; page: number; size: number }) =>
    sysPost<PageResponse<SysOrg>>(SYS_ORG_API.LIST, data),
  create: (data: { name: string; org_code: string; org_type: string }) =>
    sysPost<DataResponse<OrgCreateData>>(SYS_ORG_API.CREATE, data),
  update: (data: { id: number; name: string; org_type: string; status: number }) =>
    sysPost<CommonResponse>(SYS_ORG_API.UPDATE, data),
  delete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_ORG_API.DELETE, data),
  deptList: (data: { org_id: number }) =>
    sysPost<DataResponse<SysDept[]>>(SYS_ORG_API.DEPT_LIST, data),
  deptCreate: (data: { org_id: number; parent_id: number; dept_name: string; sort: number }) =>
    sysPost<DataResponse>(SYS_ORG_API.DEPT_CREATE, data),
  deptUpdate: (data: { id: number; dept_name: string; parent_id: number; sort: number }) =>
    sysPost<CommonResponse>(SYS_ORG_API.DEPT_UPDATE, data),
  deptDelete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_ORG_API.DEPT_DELETE, data),
}

export const sysResourceApi = {
  list: (data: { name?: string; page: number; size: number }) =>
    sysPost<PageResponse<SysResource>>(SYS_RESOURCE_API.LIST, data),
  menuList: () =>
    sysPost<DataResponse<SysResource[]>>(SYS_RESOURCE_API.MENU_LIST, {}),
  agentList: () =>
    sysPost<DataResponse<SysResource[]>>(SYS_RESOURCE_API.AGENT_LIST, {}),
  create: (data: {
    pid: number; name: string; type: number; path?: string;
    perm_code?: string; icon?: string; visible: number; sort: number
  }) => sysPost<DataResponse>(SYS_RESOURCE_API.CREATE, data),
  update: (data: {
    id: number; pid: number; name: string; type: number; path?: string;
    perm_code?: string; icon?: string; visible: number; sort: number
  }) => sysPost<CommonResponse>(SYS_RESOURCE_API.UPDATE, data),
  delete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_RESOURCE_API.DELETE, data),
}

export const sysRoleApi = {
  list: (data: { org_id: number; name?: string; page: number; size: number }) =>
    sysPost<PageResponse<SysRole>>(SYS_ROLE_API.LIST, data),
  create: (data: { org_id: number; name: string; role_type?: string }) =>
    sysPost<DataResponse>(SYS_ROLE_API.CREATE, data),
  update: (data: { id: number; name: string; status: number; role_type?: string }) =>
    sysPost<CommonResponse>(SYS_ROLE_API.UPDATE, data),
  delete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_ROLE_API.DELETE, data),
  getResources: (data: { role_id: number }) =>
    sysPost<DataResponse<number[]>>(SYS_ROLE_API.RESOURCES, data),
  assignResources: (data: { role_id: number; resource_ids: number[] }) =>
    sysPost<CommonResponse>(SYS_ROLE_API.ASSIGN_RESOURCES, data),
}

export const sysApiKeyApi = {
  list: (data: { user_id: number }) =>
    sysPost<DataResponse<SysApiKey[]>>(SYS_API_KEY_API.LIST, data),
  create: (data: { user_id: number; name: string }) =>
    sysPost<DataResponse<SysApiKey>>(SYS_API_KEY_API.CREATE, data),
  delete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_API_KEY_API.DELETE, data),
}

export const sysUserApi = {
  list: (data: { org_id: number; username?: string; real_name?: string; page: number; size: number }) =>
    sysPost<PageResponse<SysUser>>(SYS_USER_API.LIST, data),
  create: (data: { org_id: number; username: string; password: string; real_name?: string; dept_id?: number }) =>
    sysPost<DataResponse>(SYS_USER_API.CREATE, data),
  update: (data: { id: number; real_name?: string; dept_id?: number; status: number }) =>
    sysPost<CommonResponse>(SYS_USER_API.UPDATE, data),
  delete: (data: { id: number }) =>
    sysPost<CommonResponse>(SYS_USER_API.DELETE, data),
  resetPassword: (data: { id: number; new_password: string }) =>
    sysPost<CommonResponse>(SYS_USER_API.RESET_PASSWORD, data),
  getRoles: (data: { user_id: number }) =>
    sysPost<DataResponse<number[]>>(SYS_USER_API.ROLES, data),
  assignRoles: (data: { user_id: number; role_ids: number[] }) =>
    sysPost<CommonResponse>(SYS_USER_API.ASSIGN_ROLES, data),
}
