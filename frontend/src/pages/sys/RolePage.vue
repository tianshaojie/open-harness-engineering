<template>
  <div class="sys-container">
    <div class="sys-view px-6 py-4 bg-white">
      <header class="flex justify-between mb-3">
        <h1 class="text-lg font-bold tracking-tight">角色管理</h1>
        <Button @click="openCreateDialog" class="flex items-center gap-2 h-9">
          <PlusIcon class="w-4 h-4" />
          新建角色
        </Button>
      </header>

      <DataTable
        :data="roleList"
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
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openAssignDialog(row as any)">
              角色权限
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2" @click="openEditDialog(row as any)">
              编辑
            </Button>
            <Button variant="ghost" size="sm" class="h-7 px-2 text-destructive hover:text-destructive" @click="confirmDelete(row as any)">
              删除
            </Button>
          </div>
        </template>
      </DataTable>
    </div>

    <Dialog v-model:open="showDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader>
          <DialogTitle>{{ editingItem ? '编辑角色' : '新建角色' }}</DialogTitle>
        </DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">所属组织 <span class="text-destructive">*</span></label>
            <select
              :value="form.org_id"
              @change="form.org_id = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
              :disabled="!!editingItem"
            >
              <option :value="0">请选择组织</option>
              <option v-for="org in orgList" :key="org.id" :value="org.id">{{ org.name }}</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">角色名称 <span class="text-destructive">*</span></label>
            <Input v-model="form.name" placeholder="请输入角色名称" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">角色类型 <span class="text-destructive">*</span></label>
            <select
              :value="form.role_type"
              @change="form.role_type = ($event.target as HTMLSelectElement).value"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option value="normal">普通角色</option>
              <option value="admin">组织管理员</option>
            </select>
          </div>
          <div v-if="editingItem" class="space-y-1.5">
            <label class="text-sm font-medium">状态</label>
            <select
              :value="form.status"
              @change="form.status = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="1">正常</option>
              <option :value="0">禁用</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showDialog = false">取消</Button>
          <Button @click="submitForm" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showAssignDialog">
      <DialogContent class="sm:max-w-[600px] max-h-[82vh] flex flex-col p-0 gap-0 [&>button]:hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <h2 class="text-base font-semibold">分配权限 - {{ assigningRole?.name }}</h2>
          <button @click="showAssignDialog = false" class="text-gray-400 hover:text-gray-600">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        <!-- Tab 切换 -->
        <div class="flex border-b">
          <button
            v-for="tab in assignTabs" :key="tab.key"
            @click="activeAssignTab = tab.key"
            class="px-5 py-2.5 text-sm font-medium transition-colors border-b-2 -mb-px"
            :class="activeAssignTab === tab.key
              ? 'border-primary text-primary'
              : 'border-transparent text-muted-foreground hover:text-foreground'"
          >
            {{ tab.label }}
            <span class="ml-1.5 text-xs bg-muted text-muted-foreground rounded-full px-1.5 py-0.5">
              {{ tab.key === 'menu' ? selectedMenuIds.length : selectedAgentIds.length }}
            </span>
          </button>
        </div>
        <!-- 菜单权限 Tab -->
        <div v-show="activeAssignTab === 'menu'" class="flex-1 overflow-y-auto px-6 py-3">
          <div class="space-y-1">
            <label class="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-muted/50 cursor-pointer">
              <input type="checkbox" :checked="isAllMenuSelected" @change="toggleAllMenu" class="rounded" />
              <span class="text-sm font-medium">全选菜单</span>
            </label>
            <template v-for="node in menuResourceTree" :key="node.id">
              <ResourceCheckNode
                :node="node"
                :selected-ids="selectedMenuIds"
                @toggle="toggleMenuResource"
              />
            </template>
            <p v-if="menuResourceList.length === 0" class="text-sm text-muted-foreground text-center py-6">暂无菜单资源，请先在「菜单管理」中添加</p>
          </div>
        </div>
        <!-- 智能体权限 Tab -->
        <div v-show="activeAssignTab === 'agent'" class="flex-1 overflow-y-auto px-6 py-3">
          <div class="space-y-1">
            <label class="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-muted/50 cursor-pointer">
              <input type="checkbox" :checked="isAllAgentSelected" @change="toggleAllAgent" class="rounded" />
              <span class="text-sm font-medium">全选智能体</span>
            </label>
            <label
              v-for="agent in agentResourceList" :key="agent.id"
              class="flex items-center gap-2 px-2 py-2 rounded hover:bg-muted/50 cursor-pointer"
            >
              <input
                type="checkbox"
                :checked="selectedAgentIds.includes(agent.id)"
                @change="toggleAgentResource(agent.id)"
                class="rounded"
              />
              <BotIcon class="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
              <span class="text-sm">{{ agent.name }}</span>
              <span class="text-xs text-muted-foreground font-mono ml-auto">{{ agent.perm_code }}</span>
            </label>
            <p v-if="agentResourceList.length === 0" class="text-sm text-muted-foreground text-center py-6">暂无智能体资源，请先执行数据迁移同步</p>
          </div>
        </div>
        <div class="px-6 py-4 border-t flex justify-end gap-2">
          <Button variant="outline" @click="showAssignDialog = false">取消</Button>
          <Button @click="submitAssign" :disabled="submitting">{{ submitting ? '保存中...' : '保存权限' }}</Button>
        </div>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showDeleteDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>删除确认</DialogTitle></DialogHeader>
        <p class="text-sm text-muted-foreground py-2">确定要删除角色 "{{ deletingName }}" 吗？</p>
        <DialogFooter>
          <Button variant="outline" @click="showDeleteDialog = false">取消</Button>
          <Button variant="destructive" @click="doDelete" :disabled="submitting">删除</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import DataTable from '@/components/DataTable/index.vue'
import { Button } from '@/components/ui/button'
import Input from '@/components/ui/input/Input.vue'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { useToast } from '@/components/ui/toast/use-toast'
import { PlusIcon, XIcon, BotIcon } from 'lucide-vue-next'
import { sysRoleApi, sysOrgApi, sysResourceApi } from '@/api/sys'
import type { SysRole, SysOrg, SysResource } from '@/api/sys/types'
import ResourceCheckNode from '@/components/sys/ResourceCheckNode.vue'
import { formatDateTime } from '@/utils/dateUtils'

const { toast } = useToast()

const roleList = ref<SysRole[]>([])
const total = ref(0)
const submitting = ref(false)
const orgList = ref<SysOrg[]>([])
const resourceList = ref<SysResource[]>([])

const pagination = reactive({ page: 1, size: 20 })
const searchParams = reactive({ org_id: 0, name: '' })

const showDialog = ref(false)
const editingItem = ref<SysRole | null>(null)
const form = reactive({ org_id: 0, name: '', role_type: 'normal', status: 1 })

const showAssignDialog = ref(false)
const assigningRole = ref<SysRole | null>(null)
const selectedResourceIds = ref<number[]>([])

const activeAssignTab = ref<'menu' | 'agent'>('menu')
const assignTabs = [
  { key: 'agent' as const, label: '智能体权限' },
  { key: 'menu' as const, label: '菜单权限' },
]
const menuResourceList = ref<SysResource[]>([])
const agentResourceList = ref<SysResource[]>([])
const selectedMenuIds = ref<number[]>([])
const selectedAgentIds = ref<number[]>([])

const showDeleteDialog = ref(false)
const deletingName = ref('')
const deletingId = ref(0)

const searchFields = [
  { key: 'name', label: '角色名称', type: 'input' as const, placeholder: '请输入角色名称' },
]

const columns = [
  { key: 'id', title: 'ID', width: '60px' },
  { key: 'name', title: '角色名称' },
  { 
    key: 'role_type', 
    title: '角色类型', 
    render: (v: string | null) => {
      if (v === 'superadmin') return '超级管理员'
      if (v === 'admin') return '组织管理员'
      if (v === 'normal') return '普通角色'
      return '-'
    }
  },
  { key: 'status', title: '状态', width: '70px', slot: 'status' },
  { key: 'create_time', title: '创建时间', render: (v: string) => v ? formatDateTime(v) : '-' },
  { key: 'actions', title: '操作', headerAlign: 'center' as const, align: 'center' as const, slot: 'actions' },
]

const resourceTree = computed(() => buildTree(resourceList.value, 0))
const allResourceIds = computed(() => resourceList.value.map(r => r.id))
const isAllSelected = computed(() =>
  allResourceIds.value.length > 0 && allResourceIds.value.every(id => selectedResourceIds.value.includes(id))
)

const menuResourceTree = computed(() => buildTree(menuResourceList.value, 0))
const isAllMenuSelected = computed(() =>
  menuResourceList.value.length > 0 && menuResourceList.value.every(r => selectedMenuIds.value.includes(r.id))
)
const isAllAgentSelected = computed(() =>
  agentResourceList.value.length > 0 && agentResourceList.value.every(r => selectedAgentIds.value.includes(r.id))
)

function buildTree(list: SysResource[], pid: number): any[] {
  return list.filter(r => r.pid === pid).sort((a, b) => a.sort - b.sort)
    .map(r => ({ ...r, children: buildTree(list, r.id) }))
}

function toggleAll() {
  if (isAllSelected.value) {
    selectedResourceIds.value = []
  } else {
    selectedResourceIds.value = [...allResourceIds.value]
  }
}

function toggleResource(id: number) {
  const idx = selectedResourceIds.value.indexOf(id)
  if (idx >= 0) {
    selectedResourceIds.value.splice(idx, 1)
  } else {
    selectedResourceIds.value.push(id)
  }
}

function toggleMenuResource(id: number) {
  const idx = selectedMenuIds.value.indexOf(id)
  const isCurrentlySelected = idx >= 0
  
  // 获取当前节点及其所有子节点的 ID
  const getAllChildIds = (nodeId: number): number[] => {
    const node = menuResourceList.value.find(r => r.id === nodeId)
    if (!node) return [nodeId]
    
    const childIds = menuResourceList.value
      .filter(r => r.pid === nodeId)
      .flatMap(child => getAllChildIds(child.id))
    
    return [nodeId, ...childIds]
  }
  
  const affectedIds = getAllChildIds(id)
  
  if (isCurrentlySelected) {
    // 取消选中：移除当前节点及其所有子节点
    selectedMenuIds.value = selectedMenuIds.value.filter(selectedId => !affectedIds.includes(selectedId))
  } else {
    // 选中：添加当前节点及其所有子节点
    const newIds = affectedIds.filter(affectedId => !selectedMenuIds.value.includes(affectedId))
    selectedMenuIds.value.push(...newIds)
  }
}

function toggleAllMenu() {
  if (isAllMenuSelected.value) selectedMenuIds.value = []
  else selectedMenuIds.value = menuResourceList.value.map(r => r.id)
}

function toggleAgentResource(id: number) {
  const idx = selectedAgentIds.value.indexOf(id)
  if (idx >= 0) selectedAgentIds.value.splice(idx, 1)
  else selectedAgentIds.value.push(id)
}

function toggleAllAgent() {
  if (isAllAgentSelected.value) selectedAgentIds.value = []
  else selectedAgentIds.value = agentResourceList.value.map(r => r.id)
}

async function loadRoles() {
  const res = await sysRoleApi.list({
    org_id: searchParams.org_id || 0,
    name: searchParams.name || undefined,
    page: pagination.page,
    size: pagination.size,
  })
  if (res.success) { roleList.value = res.data; total.value = res.total }
}

async function loadOrgs() {
  const res = await sysOrgApi.list({ page: 1, size: 100 })
  if (res.success) orgList.value = res.data
}

async function loadResources() {
  const res = await sysResourceApi.list({ page: 1, size: 200 })
  if (res.success) resourceList.value = res.data
}

async function loadMenuAndAgentResources() {
  const [menuRes, agentRes] = await Promise.all([
    sysResourceApi.menuList(),
    sysResourceApi.agentList(),
  ])
  if (menuRes.success) menuResourceList.value = menuRes.data as SysResource[]
  if (agentRes.success) agentResourceList.value = agentRes.data as SysResource[]
}

function handleSearch(params: Record<string, any>) {
  Object.assign(searchParams, params)
  pagination.page = 1
  loadRoles()
}

function handlePageChange(page: number) { pagination.page = page; loadRoles() }
function handlePageSizeChange(size: number) { pagination.size = size; pagination.page = 1; loadRoles() }

function openCreateDialog() {
  editingItem.value = null
  Object.assign(form, { org_id: orgList.value[0]?.id || 0, name: '', role_type: 'normal', status: 1 })
  showDialog.value = true
}

function openEditDialog(item: SysRole) {
  editingItem.value = item
  Object.assign(form, { org_id: item.org_id, name: item.name, role_type: (item as any).role_type || 'normal', status: item.status })
  showDialog.value = true
}

async function submitForm() {
  if (!form.name.trim()) { toast({ title: '请输入角色名称', variant: 'destructive' }); return }
  submitting.value = true
  try {
    let res
    if (editingItem.value) {
      res = await sysRoleApi.update({ id: editingItem.value.id, name: form.name, status: form.status, role_type: form.role_type })
    } else {
      if (!form.org_id) { toast({ title: '请选择组织', variant: 'destructive' }); return }
      res = await sysRoleApi.create({ org_id: form.org_id, name: form.name, role_type: form.role_type })
    }
    if (res.success) {
      toast({ title: editingItem.value ? '更新成功' : '创建成功', variant: 'success' })
      showDialog.value = false
      loadRoles()
    } else {
      toast({ title: res.message || '操作失败', variant: 'destructive' })
    }
  } finally { submitting.value = false }
}

async function openAssignDialog(role: SysRole) {
  assigningRole.value = role
  activeAssignTab.value = 'agent'
  await loadMenuAndAgentResources()
  const res = await sysRoleApi.getResources({ role_id: role.id })
  const allIds: number[] = res.success ? (res.data as number[]) : []
  selectedResourceIds.value = allIds
  const menuIds = new Set(menuResourceList.value.map(r => r.id))
  const agentIds = new Set(agentResourceList.value.map(r => r.id))
  selectedMenuIds.value = allIds.filter(id => menuIds.has(id))
  selectedAgentIds.value = allIds.filter(id => agentIds.has(id))
  showAssignDialog.value = true
}

async function submitAssign() {
  if (!assigningRole.value) return
  submitting.value = true
  try {
    const mergedIds = [...new Set([...selectedMenuIds.value, ...selectedAgentIds.value])]
    const res = await sysRoleApi.assignResources({
      role_id: assigningRole.value.id,
      resource_ids: mergedIds,
    })
    if (res.success) {
      toast({ title: '权限分配成功', variant: 'success' })
      showAssignDialog.value = false
    }
  } finally { submitting.value = false }
}

function confirmDelete(item: SysRole) {
  deletingName.value = item.name
  deletingId.value = item.id
  showDeleteDialog.value = true
}

async function doDelete() {
  submitting.value = true
  try {
    const res = await sysRoleApi.delete({ id: deletingId.value })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      showDeleteDialog.value = false
      loadRoles()
    }
  } finally { submitting.value = false }
}

onMounted(() => {
  loadOrgs()
  loadRoles()
})
</script>

<style scoped>
.sys-container { height: calc(100vh - 44px); overflow: hidden; }
.sys-view { display: flex; flex-direction: column; height: 100%; }
</style>
