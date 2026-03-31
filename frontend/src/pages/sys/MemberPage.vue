<template>
  <div class="sys-container">
    <div class="sys-view px-6 py-4 bg-white">
      <header class="flex justify-between mb-3">
        <h1 class="text-lg font-bold tracking-tight">人员管理</h1>
        <Button @click="openCreateDialog" class="flex items-center gap-2 h-9">
          <PlusIcon class="w-4 h-4" />
          新建人员
        </Button>
      </header>

      <DataTable
        :data="userList"
        :total="total"
        :current-page="pagination.page"
        :page-size="pagination.size"
        :columns="columns"
        :search-fields="searchFields"
        :initial-search-params="searchParams"
        :show-search="true"
        :show-pagination="true"
        @search="handleSearch"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #status="{ row }">
          <span
            class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
            :class="row.status === 1 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'"
          >
            {{ row.status === 1 ? '正常' : '禁用' }}
          </span>
        </template>
        <template #actions="{ row }">
          <div class="flex items-center justify-center gap-1">
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openAssignRoleDialog(row as any)">
              分配角色
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openApiKeyDialog(row as any)">
              API密钥
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openEditDialog(row as any)">
              编辑
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openResetPwdDialog(row as any)">
              重置密码
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2 text-destructive hover:text-destructive" @click="confirmDelete(row as any)">
              删除
            </Button>
          </div>
        </template>
      </DataTable>
    </div>

    <Dialog v-model:open="showCreateDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader><DialogTitle>新建人员</DialogTitle></DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">所属组织 <span class="text-destructive">*</span></label>
            <select
              :value="createForm.org_id"
              @change="createForm.org_id = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="0">请选择组织</option>
              <option v-for="org in orgList" :key="org.id" :value="org.id">{{ org.name }}</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">登录账号 <span class="text-destructive">*</span></label>
            <Input v-model="createForm.username" placeholder="请输入登录账号" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">真实姓名</label>
            <Input v-model="createForm.real_name" placeholder="请输入真实姓名" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">初始密码 <span class="text-destructive">*</span></label>
            <Input v-model="createForm.password" type="password" placeholder="请输入初始密码" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showCreateDialog = false">取消</Button>
          <Button @click="submitCreate" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showEditDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader><DialogTitle>编辑人员</DialogTitle></DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">真实姓名</label>
            <Input v-model="editForm.real_name" placeholder="请输入真实姓名" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">状态</label>
            <select
              :value="editForm.status"
              @change="editForm.status = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="1">正常</option>
              <option :value="0">禁用</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showEditDialog = false">取消</Button>
          <Button @click="submitEdit" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showResetPwdDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>重置密码</DialogTitle></DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">新密码 <span class="text-destructive">*</span></label>
            <Input v-model="newPassword" type="password" placeholder="请输入新密码" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showResetPwdDialog = false">取消</Button>
          <Button @click="submitResetPwd" :disabled="submitting">{{ submitting ? '重置中...' : '确认重置' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showAssignRoleDialog">
      <DialogContent class="sm:max-w-[480px] max-h-[70vh] flex flex-col p-0 gap-0 [&>button]:hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <h2 class="text-base font-semibold">分配角色 - {{ assigningUser?.username }}</h2>
          <button @click="showAssignRoleDialog = false" class="text-gray-400 hover:text-gray-600">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        <div class="flex-1 overflow-y-auto px-6 py-4 space-y-1">
          <label
            v-for="role in availableRoles"
            :key="role.id"
            class="flex items-center gap-2 px-2 py-2 rounded hover:bg-muted/50 cursor-pointer"
          >
            <input
              type="checkbox"
              :checked="selectedRoleIds.includes(role.id)"
              @change="toggleRole(role.id)"
              class="rounded"
            />
            <span class="text-sm">{{ role.name }}</span>
          </label>
          <p v-if="availableRoles.length === 0" class="text-sm text-muted-foreground text-center py-4">
            该组织暂无角色，请先创建角色
          </p>
        </div>
        <div class="px-6 py-4 border-t flex justify-end gap-2">
          <Button variant="outline" @click="showAssignRoleDialog = false">取消</Button>
          <Button @click="submitAssignRole" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </div>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showDeleteDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>删除确认</DialogTitle></DialogHeader>
        <p class="text-sm text-muted-foreground py-2">确定要删除用户 "{{ deletingName }}" 吗？</p>
        <DialogFooter>
          <Button variant="outline" @click="showDeleteDialog = false">取消</Button>
          <Button variant="destructive" @click="doDelete" :disabled="submitting">删除</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- API密钥管理弹窗 -->
    <Dialog v-model:open="showApiKeyDialog">
      <DialogContent class="sm:max-w-[580px] max-h-[80vh] flex flex-col p-0 gap-0 [&>button]:hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <h2 class="text-base font-semibold">API密钥 - {{ apiKeyUser?.username }}</h2>
          <button @click="showApiKeyDialog = false" class="text-gray-400 hover:text-gray-600">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        <div class="flex-1 overflow-y-auto px-6 py-4">
          <div v-if="apiKeyList.length === 0" class="text-sm text-muted-foreground text-center py-8">暂无 API 密钥</div>
          <table v-else class="w-full text-sm">
            <thead>
              <tr class="border-b text-muted-foreground">
                <th class="text-left py-2 font-medium">名称</th>
                <th class="text-left py-2 font-medium">密钥</th>
                <th class="text-left py-2 font-medium">最后使用</th>
                <th class="text-right py-2 font-medium">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="key in apiKeyList" :key="key.id" class="border-b last:border-0">
                <td class="py-2">{{ key.name }}</td>
                <td class="py-2 font-mono text-xs">{{ maskApiKey(key.api_key) }}</td>
                <td class="py-2 text-muted-foreground">{{ key.last_use_time ? formatDateTime(key.last_use_time) : '从未使用' }}</td>
                <td class="py-2 text-right">
                  <button @click="copyText(key.api_key)" class="text-muted-foreground hover:text-foreground mr-3" title="复制">
                    <CopyIcon class="w-3.5 h-3.5 inline" />
                  </button>
                  <button @click="confirmDeleteApiKey(key)" class="text-destructive hover:text-destructive/80" title="删除">
                    <TrashIcon class="w-3.5 h-3.5 inline" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="px-6 py-4 border-t flex items-center gap-3">
          <Input v-model="newApiKeyName" placeholder="输入密钥名称" class="flex-1" @keyup.enter="doCreateApiKey" />
          <Button @click="doCreateApiKey" :disabled="!newApiKeyName.trim() || submitting">创建密钥</Button>
          <Button variant="outline" @click="showApiKeyDialog = false">关闭</Button>
        </div>
      </DialogContent>
    </Dialog>

    <!-- 删除 API密钥确认弹窗 -->
    <Dialog v-model:open="showDeleteApiKeyDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>删除确认</DialogTitle></DialogHeader>
        <p class="text-sm text-muted-foreground py-2">确定要删除密钥 "{{ deletingApiKey?.name }}" 吗？</p>
        <DialogFooter>
          <Button variant="outline" @click="showDeleteApiKeyDialog = false">取消</Button>
          <Button variant="destructive" @click="doDeleteApiKey" :disabled="submitting">删除</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import DataTable from '@/components/DataTable/index.vue'
import { Button } from '@/components/ui/button'
import Input from '@/components/ui/input/Input.vue'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { useToast } from '@/components/ui/toast/use-toast'
import { PlusIcon, XIcon, CopyIcon, TrashIcon } from 'lucide-vue-next'
import { sysUserApi, sysOrgApi, sysRoleApi, sysApiKeyApi } from '@/api/sys'
import type { SysUser, SysOrg, SysRole, SysApiKey } from '@/api/sys/types'
import { formatDateTime } from '@/utils/dateUtils'

const { toast } = useToast()

const userList = ref<SysUser[]>([])
const total = ref(0)
const submitting = ref(false)
const orgList = ref<SysOrg[]>([])
const availableRoles = ref<SysRole[]>([])

const pagination = reactive({ page: 1, size: 20 })
const searchParams = reactive({ org_id: 0, username: '', real_name: '' })

const showCreateDialog = ref(false)
const createForm = reactive({ org_id: 0, username: '', real_name: '', password: '' })

const showEditDialog = ref(false)
const editingUser = ref<SysUser | null>(null)
const editForm = reactive({ real_name: '', status: 1 })

const showResetPwdDialog = ref(false)
const resetPwdUserId = ref(0)
const newPassword = ref('')

const showAssignRoleDialog = ref(false)
const assigningUser = ref<SysUser | null>(null)
const selectedRoleIds = ref<number[]>([])

const showDeleteDialog = ref(false)
const deletingName = ref('')
const deletingId = ref(0)

const showApiKeyDialog = ref(false)
const apiKeyUser = ref<SysUser | null>(null)
const apiKeyList = ref<SysApiKey[]>([])
const newApiKeyName = ref('')
const showDeleteApiKeyDialog = ref(false)
const deletingApiKey = ref<SysApiKey | null>(null)

const searchFields = [
  { key: 'username', label: '账号', type: 'input' as const, placeholder: '请输入账号' },
  { key: 'real_name', label: '姓名', type: 'input' as const, placeholder: '请输入姓名' },
]

const columns = [
  { key: 'id', title: 'ID', width: '60px' },
  { key: 'username', title: '登录账号' },
  { key: 'real_name', title: '真实姓名', render: (v: string | null) => v || '-' },
  { key: 'roles', title: '角色', render: (v: string | null) => v || '-' },
  { key: 'status', title: '状态', width: '70px', slot: 'status' },
  { key: 'create_time', title: '创建时间', render: (v: string) => v ? formatDateTime(v) : '-' },
  { key: 'actions', title: '操作', headerAlign: 'center' as const, align: 'center' as const, slot: 'actions' },
]

async function loadUsers() {
  const res = await sysUserApi.list({
    org_id: searchParams.org_id || 0,
    username: searchParams.username || undefined,
    real_name: searchParams.real_name || undefined,
    page: pagination.page,
    size: pagination.size,
  })
  if (res.success) { userList.value = res.data; total.value = res.total }
}

async function loadOrgs() {
  const res = await sysOrgApi.list({ page: 1, size: 100 })
  if (res.success) orgList.value = res.data
}

function handleSearch(params: Record<string, any>) {
  Object.assign(searchParams, params)
  pagination.page = 1
  loadUsers()
}

function handlePageChange(page: number) { pagination.page = page; loadUsers() }
function handlePageSizeChange(size: number) { pagination.size = size; pagination.page = 1; loadUsers() }

function openCreateDialog() {
  Object.assign(createForm, { org_id: orgList.value[0]?.id || 0, username: '', real_name: '', password: '' })
  showCreateDialog.value = true
}

async function submitCreate() {
  if (!createForm.username.trim()) { toast({ title: '请输入账号', variant: 'destructive' }); return }
  if (!createForm.password.trim()) { toast({ title: '请输入密码', variant: 'destructive' }); return }
  if (!createForm.org_id) { toast({ title: '请选择组织', variant: 'destructive' }); return }
  submitting.value = true
  try {
    const res = await sysUserApi.create({
      org_id: createForm.org_id,
      username: createForm.username,
      password: createForm.password,
      real_name: createForm.real_name || undefined,
    })
    if (res.success) {
      toast({ title: '创建成功', variant: 'success' })
      showCreateDialog.value = false
      loadUsers()
    }
  } finally { submitting.value = false }
}

function openEditDialog(user: SysUser) {
  editingUser.value = user
  Object.assign(editForm, { real_name: user.real_name || '', status: user.status })
  showEditDialog.value = true
}

async function submitEdit() {
  if (!editingUser.value) return
  submitting.value = true
  try {
    const res = await sysUserApi.update({
      id: editingUser.value.id,
      real_name: editForm.real_name || undefined,
      status: editForm.status,
    })
    if (res.success) {
      toast({ title: '更新成功', variant: 'success' })
      showEditDialog.value = false
      loadUsers()
    }
  } finally { submitting.value = false }
}

function openResetPwdDialog(user: SysUser) {
  resetPwdUserId.value = user.id
  newPassword.value = ''
  showResetPwdDialog.value = true
}

async function submitResetPwd() {
  if (!newPassword.value.trim()) { toast({ title: '请输入新密码', variant: 'destructive' }); return }
  submitting.value = true
  try {
    const res = await sysUserApi.resetPassword({ id: resetPwdUserId.value, new_password: newPassword.value })
    if (res.success) {
      toast({ title: '密码重置成功', variant: 'success' })
      showResetPwdDialog.value = false
    }
  } finally { submitting.value = false }
}

async function openAssignRoleDialog(user: SysUser) {
  assigningUser.value = user
  const rolesRes = await sysRoleApi.list({ org_id: user.org_id, page: 1, size: 100 })
  availableRoles.value = rolesRes.success ? rolesRes.data : []
  const userRolesRes = await sysUserApi.getRoles({ user_id: user.id })
  selectedRoleIds.value = userRolesRes.success ? (userRolesRes.data as number[]) : []
  showAssignRoleDialog.value = true
}

function toggleRole(id: number) {
  const idx = selectedRoleIds.value.indexOf(id)
  if (idx >= 0) selectedRoleIds.value.splice(idx, 1)
  else selectedRoleIds.value.push(id)
}

async function submitAssignRole() {
  if (!assigningUser.value) return
  submitting.value = true
  try {
    const res = await sysUserApi.assignRoles({ user_id: assigningUser.value.id, role_ids: selectedRoleIds.value })
    if (res.success) {
      toast({ title: '角色分配成功', variant: 'success' })
      showAssignRoleDialog.value = false
    }
  } finally { submitting.value = false }
}

function confirmDelete(user: SysUser) {
  deletingName.value = user.username
  deletingId.value = user.id
  showDeleteDialog.value = true
}

async function doDelete() {
  submitting.value = true
  try {
    const res = await sysUserApi.delete({ id: deletingId.value })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      showDeleteDialog.value = false
      loadUsers()
    }
  } finally { submitting.value = false }
}

function maskApiKey(key: string) {
  if (!key || key.length < 11) return key
  return `${key.substring(0, 7)}${'*'.repeat(Math.max(0, key.length - 11))}${key.substring(key.length - 4)}`
}

async function copyText(text: string) {
  try {
    await navigator.clipboard.writeText(text)
    toast({ title: '已复制到剪贴板', variant: 'success' })
  } catch {
    toast({ title: '复制失败', variant: 'destructive' })
  }
}

async function openApiKeyDialog(user: SysUser) {
  apiKeyUser.value = user
  newApiKeyName.value = ''
  const res = await sysApiKeyApi.list({ user_id: user.id })
  apiKeyList.value = res.success ? (res.data as SysApiKey[]) : []
  showApiKeyDialog.value = true
}

async function doCreateApiKey() {
  if (!newApiKeyName.value.trim() || !apiKeyUser.value) return
  submitting.value = true
  try {
    const res = await sysApiKeyApi.create({ user_id: apiKeyUser.value.id, name: newApiKeyName.value.trim() })
    if (res.success) {
      toast({ title: '创建成功', variant: 'success' })
      newApiKeyName.value = ''
      const listRes = await sysApiKeyApi.list({ user_id: apiKeyUser.value.id })
      apiKeyList.value = listRes.success ? (listRes.data as SysApiKey[]) : []
    } else {
      toast({ title: res.message || '创建失败', variant: 'destructive' })
    }
  } finally { submitting.value = false }
}

function confirmDeleteApiKey(key: SysApiKey) {
  deletingApiKey.value = key
  showDeleteApiKeyDialog.value = true
}

async function doDeleteApiKey() {
  if (!deletingApiKey.value || !apiKeyUser.value) return
  submitting.value = true
  try {
    const res = await sysApiKeyApi.delete({ id: deletingApiKey.value.id })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      showDeleteApiKeyDialog.value = false
      deletingApiKey.value = null
      const listRes = await sysApiKeyApi.list({ user_id: apiKeyUser.value.id })
      apiKeyList.value = listRes.success ? (listRes.data as SysApiKey[]) : []
    } else {
      toast({ title: res.message || '删除失败', variant: 'destructive' })
    }
  } finally { submitting.value = false }
}

onMounted(() => { loadOrgs(); loadUsers() })
</script>

<style scoped>
.sys-container { height: calc(100vh - 44px); overflow: hidden; }
.sys-view { display: flex; flex-direction: column; height: 100%; }
</style>
