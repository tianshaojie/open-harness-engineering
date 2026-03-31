const SYS_BASE = '/api/sys'

export const SYS_LOGIN_API = {
  LOGIN: `${SYS_BASE}/login`,
} as const

export const SYS_ORG_API = {
  LIST: `${SYS_BASE}/org/list`,
  CREATE: `${SYS_BASE}/org/create`,
  UPDATE: `${SYS_BASE}/org/update`,
  DELETE: `${SYS_BASE}/org/delete`,
  DEPT_LIST: `${SYS_BASE}/org/dept/list`,
  DEPT_CREATE: `${SYS_BASE}/org/dept/create`,
  DEPT_UPDATE: `${SYS_BASE}/org/dept/update`,
  DEPT_DELETE: `${SYS_BASE}/org/dept/delete`,
} as const

export const SYS_RESOURCE_API = {
  LIST: `${SYS_BASE}/resource/list`,
  MENU_LIST: `${SYS_BASE}/resource/menu-list`,
  AGENT_LIST: `${SYS_BASE}/resource/agent-list`,
  CREATE: `${SYS_BASE}/resource/create`,
  UPDATE: `${SYS_BASE}/resource/update`,
  DELETE: `${SYS_BASE}/resource/delete`,
} as const

export const SYS_ROLE_API = {
  LIST: `${SYS_BASE}/role/list`,
  CREATE: `${SYS_BASE}/role/create`,
  UPDATE: `${SYS_BASE}/role/update`,
  DELETE: `${SYS_BASE}/role/delete`,
  RESOURCES: `${SYS_BASE}/role/resources`,
  ASSIGN_RESOURCES: `${SYS_BASE}/role/assign_resources`,
} as const

export const SYS_USER_API = {
  LIST: `${SYS_BASE}/user/list`,
  CREATE: `${SYS_BASE}/user/create`,
  UPDATE: `${SYS_BASE}/user/update`,
  DELETE: `${SYS_BASE}/user/delete`,
  RESET_PASSWORD: `${SYS_BASE}/user/reset_password`,
  ROLES: `${SYS_BASE}/user/roles`,
  ASSIGN_ROLES: `${SYS_BASE}/user/assign_roles`,
} as const

export const SYS_API_KEY_API = {
  LIST: `${SYS_BASE}/user/api_key/list`,
  CREATE: `${SYS_BASE}/user/api_key/create`,
  DELETE: `${SYS_BASE}/user/api_key/delete`,
} as const
