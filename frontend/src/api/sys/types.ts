export interface CommonResponse {
  success: boolean
  message: string
}

export interface PageResponse<T = any> extends CommonResponse {
  data: T[]
  total: number
  page: number
  size: number
}

export interface DataResponse<T = any> extends CommonResponse {
  data: T
}

export interface SysLoginRequest {
  username: string
  password: string
}

export interface SysLoginData {
  token: string
  user_id: number
  org_id: number
  username: string
  real_name: string | null
}

export interface SysLoginResponse extends CommonResponse {
  data: SysLoginData | null
}

export interface OrgCreateData {
  id: number
  admin_username: string
  admin_password: string
}

export interface SysOrg {
  id: number
  name: string
  org_code: string
  org_type: string
  status: number
  create_time: string | null
  update_time: string | null
}

export interface SysDept {
  id: number
  org_id: number
  parent_id: number
  dept_name: string
  sort: number
  create_time: string | null
}

export interface SysResource {
  id: number
  org_id: number | null
  pid: number
  name: string
  type: number
  path: string | null
  perm_code: string | null
  icon: string | null
  visible: number
  sort: number
  status: number
  create_time: string | null
}

export interface SysRole {
  id: number
  org_id: number
  name: string
  role_type?: string
  status: number
  create_time: string | null
}

export interface SysUser {
  id: number
  org_id: number
  dept_id: number | null
  username: string
  real_name: string | null
  status: number
  create_time: string | null
  roles: string | null
}

export interface SysApiKey {
  id: number
  user_id: number
  name: string
  api_key: string
  last_use_time: string | null
  create_user: { id: number; username: string } | null
  create_time: string
  update_time: string
}
