<template>
  <div class="sys-container">
    <div class="sys-view px-6 py-4 bg-white">
      <header class="flex justify-between items-center mb-4">
        <h1 class="text-lg font-bold tracking-tight">组织与成员</h1>
        <Button v-if="isSuperadmin" @click="openCreateOrgDialog" class="flex items-center gap-2 h-9">
          <PlusIcon class="w-4 h-4" />
          新建组织
        </Button>
      </header>

      <div class="flex gap-3 flex-1 min-h-0">

        <!-- 第一栏：组织列表（仅 superadmin） -->
        <div v-if="isSuperadmin" class="w-52 flex-shrink-0 border border-border rounded-lg overflow-hidden flex flex-col">
          <div class="px-3 h-9 bg-white border-b border-border flex items-center">
            <span class="text-xs font-semibold text-muted-foreground tracking-wide">组织</span>
          </div>
          <div class="flex-1 overflow-y-auto">
            <div
              v-for="org in orgList"
              :key="org.id"
              class="flex items-center justify-between px-3 py-2 cursor-pointer hover:bg-muted/50 border-b border-border/40 last:border-0 transition-colors group"
              :class="selectedOrg?.id === org.id ? 'bg-accent text-accent-foreground' : ''"
              @click="selectOrg(org)"
            >
              <div class="flex items-center gap-2 min-w-0">
                <Building2Icon class="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
                <span class="text-sm truncate">{{ org.name }}</span>
              </div>
              <div class="flex items-center gap-0.5 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                <Button variant="ghost" size="sm" class="h-5 w-5 p-0" @click.stop="openEditOrgDialog(org)">
                  <PencilIcon class="w-3 h-3" />
                </Button>
                <Button variant="ghost" size="sm" class="h-5 w-5 p-0 text-destructive hover:text-destructive" @click.stop="confirmDeleteOrg(org)">
                  <Trash2Icon class="w-3 h-3" />
                </Button>
              </div>
            </div>
            <div v-if="orgList.length === 0" class="px-3 py-8 text-center text-xs text-muted-foreground">暂无组织</div>
          </div>
        </div>

        <!-- 第二栏：部门树 -->
        <div class="w-56 flex-shrink-0 border border-border rounded-lg overflow-hidden flex flex-col">
          <div class="px-3 h-9 bg-white border-b border-border flex items-center justify-between">
            <span class="text-xs font-semibold text-muted-foreground tracking-wide">组织部门</span>
            <Button
              v-if="selectedOrg || !isSuperadmin"
              variant="ghost" size="sm" class="h-6 w-6 p-0"
              @click="openCreateDeptDialog(0)"
            >
              <PlusIcon class="w-3 h-3" />
            </Button>
          </div>
          <div class="flex-1 overflow-y-auto p-1.5">
            <div v-if="isSuperadmin && !selectedOrg" class="flex flex-col items-center justify-center h-full gap-1 text-muted-foreground py-8">
              <Building2Icon class="w-6 h-6 opacity-30" />
              <p class="text-xs">请先选择组织</p>
            </div>
            <template v-else>
              <div v-if="deptLoading" class="flex items-center justify-center py-8">
                <div class="animate-spin w-4 h-4 border-2 border-primary border-t-transparent rounded-full"></div>
              </div>
              <template v-else>
                <!-- 组织根节点：显示未归属部门的成员 -->
                <div
                  class="flex items-center gap-1.5 px-2 py-1.5 rounded-md cursor-pointer hover:bg-[#F3F6FA] transition-colors mb-0.5"
                  @click="selectOrgRoot"
                >
                  <Building2Icon class="w-4 h-4 flex-shrink-0 text-muted-foreground" />
                  <span class="text-sm font-medium truncate text-[#1A2233]">{{ selectedOrg?.name || currentOrgName }}</span>
                </div>
                <DeptTreeNode
                  v-for="node in deptTree"
                  :key="node.id"
                  :node="node"
                  :selected-id="selectedDept?.id ?? null"
                  @add-child="openCreateDeptDialog"
                  @edit="openEditDeptDialog"
                  @delete="confirmDeleteDept"
                  @select="selectDept"
                />
              </template>
            </template>
          </div>
        </div>

        <!-- 第三栏：成员列表 -->
        <div class="flex-1 min-w-0 border border-border rounded-lg overflow-hidden flex flex-col">
          <div class="px-3 h-9 bg-white border-b border-border flex items-center justify-between">
            <span class="text-xs font-semibold text-muted-foreground tracking-wide">
              {{ selectedOrgAsRoot ? `${selectedOrg?.name || currentOrgName} · 未分部门` : selectedDept ? `${selectedDept.dept_name} · 成员` : '成员' }}
            </span>
            <Button v-if="selectedDept || selectedOrgAsRoot" variant="ghost" size="sm" class="h-6 w-6 p-0" @click="openCreateMemberDialog">
              <PlusIcon class="w-3 h-3" />
            </Button>
          </div>
          <div class="flex-1 overflow-hidden">
            <div v-if="!selectedDept && !selectedOrgAsRoot" class="flex flex-col items-center justify-center h-full gap-1 text-muted-foreground">
              <UsersIcon class="w-6 h-6 opacity-30" />
              <p class="text-xs">请先选择部门</p>
            </div>
            <DataTable
              v-else
              :data="memberList"
              :columns="memberColumns"
              :show-search="false"
              :show-pagination="false"
              :loading="memberLoading"
            >
              <template #dept="{ row }">
                <span
                  v-if="(row as any).dept_id"
                  class="inline-flex items-center gap-1 text-sm cursor-pointer hover:text-primary"
                  @click="openEditMemberDialog(row as any)"
                >
                  <FolderIcon class="w-3 h-3 text-amber-500 flex-shrink-0" />
                  {{ flatDepts.find(d => d.id === (row as any).dept_id)?.dept_name || '-' }}
                </span>
                <span v-else class="text-sm">{{ selectedOrg?.name || currentOrgName }}</span>
              </template>
              <template #status="{ row }">
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                  :class="(row as any).status === 1 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'"
                >{{ (row as any).status === 1 ? '正常' : '禁用' }}</span>
              </template>
              <template #actions="{ row }">
                <div class="flex items-center justify-end gap-0.5">
                  <Button variant="ghost" size="sm" class="h-6 px-1.5 text-xs" @click="openEditMemberDialog(row as any)">编辑</Button>
                  <Button variant="ghost" size="sm" class="h-6 px-1.5 text-xs" @click="openAssignRoleDialog(row as any)">角色</Button>
                  <Button variant="ghost" size="sm" class="h-6 px-1.5 text-xs" @click="openApiKeyDialog(row as any)">API密钥</Button>
                  <Button variant="ghost" size="sm" class="h-6 px-1.5 text-xs" @click="openResetPwdDialog(row as any)">重置密码</Button>
                  <Button variant="ghost" size="sm" class="h-6 px-1.5 text-xs text-destructive hover:text-destructive" @click="confirmDeleteMember(row as any)">删除</Button>
                </div>
              </template>
            </DataTable>
          </div>
        </div>
      </div>
    </div>

    <Dialog v-model:open="showOrgDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader>
          <DialogTitle>{{ editingOrg ? '编辑组织' : '新建组织' }}</DialogTitle>
        </DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">组织名称 <span class="text-destructive">*</span></label>
            <Input v-model="orgForm.name" placeholder="请输入组织名称" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">机构码 <span class="text-destructive">*</span></label>
            <Input v-model="orgForm.org_code" placeholder="唯一标识（小写），如 baidu" :disabled="!!editingOrg" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">类型</label>
            <select v-model="orgForm.org_type" class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm">
              <option value="COMPANY">公司</option>
              <option value="PERSONAL">个人</option>
            </select>
          </div>
          <div v-if="editingOrg" class="space-y-1.5">
            <label class="text-sm font-medium">状态</label>
            <select
              :value="orgForm.status"
              @change="orgForm.status = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="1">正常</option>
              <option :value="0">禁用</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showOrgDialog = false">取消</Button>
          <Button @click="submitOrgForm" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showDeptDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader>
          <DialogTitle>{{ editingDept ? '编辑部门' : '新建部门' }}</DialogTitle>
        </DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">部门名称 <span class="text-destructive">*</span></label>
            <Input v-model="deptForm.dept_name" placeholder="请输入部门名称" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">上级部门</label>
            <select
              :value="deptForm.parent_id"
              @change="deptForm.parent_id = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="0">{{ selectedOrg?.name || currentOrgName }}</option>
              <option v-for="d in flatDepts" :key="d.id" :value="d.id">{{ d.dept_name }}</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">排序</label>
            <input v-model.number="deptForm.sort" type="number" placeholder="0" class="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showDeptDialog = false">取消</Button>
          <Button @click="submitDeptForm" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- 新建组织成功提示 -->
    <Dialog v-model:open="showOrgCreatedDialog">
      <DialogContent class="sm:max-w-[420px]">
        <DialogHeader>
          <DialogTitle>组织创建成功</DialogTitle>
        </DialogHeader>
        <div class="space-y-3 py-2 text-sm">
          <p class="text-muted-foreground">已自动完成以下初始化：</p>
          <ul class="list-disc list-inside space-y-1 text-foreground">
            <li>创建「管理员」角色，并授予全部菜单和智能体权限</li>
            <li>创建管理员账号并绑定角色</li>
          </ul>
          <div class="bg-muted rounded-md px-4 py-3 space-y-1 font-mono text-xs">
            <div>用户名：<span class="font-semibold">{{ createdAdminInfo.username }}</span></div>
            <div>初始密码：<span class="font-semibold">{{ createdAdminInfo.password }}</span></div>
          </div>
          <p class="text-xs text-muted-foreground">请妥善保存初始密码，登录后建议立即修改。</p>
        </div>
        <DialogFooter>
          <Button @click="showOrgCreatedDialog = false">确定</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="showDeleteDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>删除确认</DialogTitle></DialogHeader>
        <p class="text-sm text-muted-foreground py-2">确定要删除 "{{ deletingName }}" 吗？此操作不可撤销。</p>
        <DialogFooter>
          <Button variant="outline" @click="showDeleteDialog = false">取消</Button>
          <Button variant="destructive" @click="confirmDelete" :disabled="submitting">删除</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- 新建成员 -->
    <Dialog v-model:open="showCreateMemberDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader><DialogTitle>新建成员</DialogTitle></DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">登录账号 <span class="text-destructive">*</span></label>
            <Input v-model="memberCreateForm.username" placeholder="请输入登录账号" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">真实姓名</label>
            <Input v-model="memberCreateForm.real_name" placeholder="请输入真实姓名" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">初始密码 <span class="text-destructive">*</span></label>
            <Input v-model="memberCreateForm.password" type="password" placeholder="请输入初始密码" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">所属部门</label>
            <select
              :value="memberCreateForm.dept_id"
              @change="memberCreateForm.dept_id = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="0">不指定</option>
              <option v-for="d in flatDepts" :key="d.id" :value="d.id">{{ d.dept_name }}</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showCreateMemberDialog = false">取消</Button>
          <Button @click="submitCreateMember" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- 编辑成员 -->
    <Dialog v-model:open="showEditMemberDialog">
      <DialogContent class="sm:max-w-[440px]">
        <DialogHeader><DialogTitle>编辑成员</DialogTitle></DialogHeader>
        <div class="space-y-4 py-2">
          <div class="space-y-1.5">
            <label class="text-sm font-medium">真实姓名</label>
            <Input v-model="memberEditForm.real_name" placeholder="请输入真实姓名" />
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">所属部门</label>
            <select
              :value="memberEditForm.dept_id"
              @change="memberEditForm.dept_id = Number(($event.target as HTMLSelectElement).value) || undefined"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="0">不指定</option>
              <option v-for="d in flatDepts" :key="d.id" :value="d.id">{{ d.dept_name }}</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-sm font-medium">状态</label>
            <select
              :value="memberEditForm.status"
              @change="memberEditForm.status = Number(($event.target as HTMLSelectElement).value)"
              class="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
            >
              <option :value="1">正常</option>
              <option :value="0">禁用</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showEditMemberDialog = false">取消</Button>
          <Button @click="submitEditMember" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- 重置密码 -->
    <Dialog v-model:open="showResetPwdDialog">
      <DialogContent class="sm:max-w-[400px]">
        <DialogHeader><DialogTitle>重置密码 - {{ resetPwdUser?.username }}</DialogTitle></DialogHeader>
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

    <!-- 分配角色 -->
    <Dialog v-model:open="showAssignRoleDialog">
      <DialogContent class="sm:max-w-[480px] max-h-[70vh] flex flex-col p-0 gap-0 [&>button]:hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <h2 class="text-base font-semibold">分配角色 - {{ assigningMember?.username }}</h2>
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
            <input type="radio" :value="role.id" v-model="selectedRoleId" class="rounded-full" />
            <span class="text-sm">{{ role.name }}</span>
          </label>
          <p v-if="availableRoles.length === 0" class="text-sm text-muted-foreground text-center py-4">该组织暂无角色</p>
        </div>
        <div class="px-6 py-4 border-t flex justify-end gap-2">
          <Button variant="outline" @click="showAssignRoleDialog = false">取消</Button>
          <Button @click="submitAssignRole" :disabled="submitting">{{ submitting ? '保存中...' : '保存' }}</Button>
        </div>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import Input from '@/components/ui/input/Input.vue'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { useToast } from '@/components/ui/toast/use-toast'
import { PlusIcon, Building2Icon, PencilIcon, Trash2Icon, NetworkIcon, UsersIcon, XIcon, ShieldCheckIcon, KeyRoundIcon, FolderIcon, CopyIcon, TrashIcon } from 'lucide-vue-next'
import { sysOrgApi, sysUserApi, sysRoleApi, sysApiKeyApi } from '@/api/sys'
import type { SysOrg, SysDept, SysUser, SysRole, SysApiKey } from '@/api/sys/types'
import { formatDateTime } from '@/utils/dateUtils'
import DeptTreeNode from '@/components/sys/DeptTreeNode.vue'
import DataTable from '@/components/DataTable/index.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isSuperadmin = authStore.userInfo?.org_id === 0 
  || localStorage.getItem('sys_isSuperAdmin') === 'true'
  || localStorage.getItem('username') === 'superadmin'
const { toast } = useToast()

const orgList = ref<SysOrg[]>([])
const selectedOrg = ref<SysOrg | null>(null)
const deptList = ref<SysDept[]>([])
const submitting = ref(false)
const deptLoading = ref(false)
const currentOrgName = ref('')

const showOrgDialog = ref(false)
const editingOrg = ref<SysOrg | null>(null)
const orgForm = reactive({ name: '', org_code: '', org_type: 'COMPANY', status: 1 })

const showDeptDialog = ref(false)
const editingDept = ref<SysDept | null>(null)
const deptForm = reactive({ dept_name: '', parent_id: 0, sort: 0 })

const showDeleteDialog = ref(false)
const deletingName = ref('')
const deleteAction = ref<(() => Promise<void>) | null>(null)

const showOrgCreatedDialog = ref(false)
const createdAdminInfo = reactive({ username: 'admin', password: 'Admin@123' })

const selectedDept = ref<SysDept | null>(null)
const selectedOrgAsRoot = ref(false)
const memberList = ref<SysUser[]>([])
const memberLoading = ref(false)

const showCreateMemberDialog = ref(false)
const memberCreateForm = reactive({ username: '', real_name: '', password: '', dept_id: 0 })

const showEditMemberDialog = ref(false)
const editingMember = ref<SysUser | null>(null)
const memberEditForm = reactive({ real_name: '', dept_id: undefined as number | undefined, status: 1 })

const showResetPwdDialog = ref(false)
const resetPwdUser = ref<SysUser | null>(null)
const newPassword = ref('')

const showAssignRoleDialog = ref(false)
const assigningMember = ref<SysUser | null>(null)
const availableRoles = ref<SysRole[]>([])
const selectedRoleId = ref<number | null>(null)

const showApiKeyDialog = ref(false)
const apiKeyUser = ref<SysUser | null>(null)
const apiKeyList = ref<SysApiKey[]>([])
const newApiKeyName = ref('')
const showDeleteApiKeyDialog = ref(false)
const deletingApiKey = ref<SysApiKey | null>(null)

const flatDepts = computed(() => deptList.value)
const deptTree = computed(() => buildTree(deptList.value, 0))

const memberColumns = [
  { key: 'username', title: '账号', width: '120px' },
  { key: 'real_name', title: '姓名', width: '100px', render: (v: string | null) => v || '-' },
  { key: 'roles', title: '角色', render: (v: string | null) => v || '-' },
  { key: 'dept_id', title: '部门', slot: 'dept' },
  { key: 'status', title: '状态', width: '70px', slot: 'status' },
  { key: 'actions', title: '操作', headerAlign: 'right' as const, align: 'right' as const, slot: 'actions' },
]

function buildTree(list: SysDept[], parentId: number): any[] {
  return list
    .filter(d => d.parent_id === parentId)
    .map(d => ({ ...d, children: buildTree(list, d.id) }))
}

async function loadOrgs() {
  const res = await sysOrgApi.list({ page: 1, size: 100 })
  if (res.success) orgList.value = res.data
}

async function loadDepts() {
  if (!selectedOrg.value) return
  const res = await sysOrgApi.deptList({ org_id: selectedOrg.value.id })
  if (res.success) deptList.value = res.data as SysDept[]
}

async function loadAdminDepts() {
  deptLoading.value = true
  try {
    const orgListRes = await sysOrgApi.list({ page: 1, size: 1 })
    if (orgListRes.success && orgListRes.data.length > 0) {
      const org = orgListRes.data[0]
      selectedOrg.value = org
      currentOrgName.value = org.name
      const res = await sysOrgApi.deptList({ org_id: org.id })
      if (res.success) deptList.value = res.data as SysDept[]
      await selectOrgRoot()
    }
  } finally {
    deptLoading.value = false
  }
}

function selectOrg(org: SysOrg) {
  selectedOrg.value = org
  selectedDept.value = null
  selectedOrgAsRoot.value = false
  memberList.value = []
  loadDepts()
}

async function selectOrgRoot() {
  selectedDept.value = null
  selectedOrgAsRoot.value = true
  memberLoading.value = true
  try {
    const res = await sysUserApi.list({ org_id: selectedOrg.value?.id || 0, page: 1, size: 200 })
    if (res.success) memberList.value = res.data.filter(u => !u.dept_id)
  } finally { memberLoading.value = false }
}

async function selectDept(dept: SysDept) {
  selectedDept.value = dept
  selectedOrgAsRoot.value = false
  memberLoading.value = true
  try {
    const res = await sysUserApi.list({ org_id: selectedOrg.value?.id || 0, page: 1, size: 200 })
    if (res.success) memberList.value = res.data.filter(u => u.dept_id === dept.id)
  } finally { memberLoading.value = false }
}

function openCreateMemberDialog() {
  Object.assign(memberCreateForm, { username: '', real_name: '', password: '', dept_id: selectedDept.value?.id || 0 })
  showCreateMemberDialog.value = true
}

async function submitCreateMember() {
  if (!memberCreateForm.username.trim()) { toast({ title: '请输入账号', variant: 'destructive' }); return }
  if (!memberCreateForm.password.trim()) { toast({ title: '请输入密码', variant: 'destructive' }); return }
  submitting.value = true
  try {
    const res = await sysUserApi.create({
      org_id: selectedOrg.value!.id,
      username: memberCreateForm.username,
      password: memberCreateForm.password,
      real_name: memberCreateForm.real_name || undefined,
      dept_id: memberCreateForm.dept_id || undefined,
    })
    if (res.success) {
      toast({ title: '创建成功', variant: 'success' })
      showCreateMemberDialog.value = false
      if (selectedDept.value) selectDept(selectedDept.value)
    }
  } finally { submitting.value = false }
}

function openEditMemberDialog(user: SysUser) {
  editingMember.value = user
  Object.assign(memberEditForm, { real_name: user.real_name || '', dept_id: user.dept_id || undefined, status: user.status })
  showEditMemberDialog.value = true
}

async function submitEditMember() {
  if (!editingMember.value) return
  submitting.value = true
  try {
    const res = await sysUserApi.update({
      id: editingMember.value.id,
      real_name: memberEditForm.real_name || undefined,
      dept_id: memberEditForm.dept_id,
      status: memberEditForm.status,
    })
    if (res.success) {
      toast({ title: '更新成功', variant: 'success' })
      showEditMemberDialog.value = false
      // 刷新成员列表
      if (selectedDept.value) {
        selectDept(selectedDept.value)
      } else if (selectedOrgAsRoot.value) {
        selectOrgRoot()
      }
    }
  } finally { submitting.value = false }
}

function openResetPwdDialog(user: SysUser) {
  resetPwdUser.value = user
  newPassword.value = ''
  showResetPwdDialog.value = true
}

async function submitResetPwd() {
  if (!newPassword.value.trim()) { toast({ title: '请输入新密码', variant: 'destructive' }); return }
  submitting.value = true
  try {
    const res = await sysUserApi.resetPassword({ id: resetPwdUser.value!.id, new_password: newPassword.value })
    if (res.success) {
      toast({ title: '密码重置成功', variant: 'success' })
      showResetPwdDialog.value = false
    }
  } finally { submitting.value = false }
}

async function openAssignRoleDialog(user: SysUser) {
  assigningMember.value = user
  const rolesRes = await sysRoleApi.list({ org_id: user.org_id, page: 1, size: 100 })
  availableRoles.value = rolesRes.success ? rolesRes.data : []
  const userRolesRes = await sysUserApi.getRoles({ user_id: user.id })
  const roleIds = userRolesRes.success ? (userRolesRes.data as number[]) : []
  selectedRoleId.value = roleIds.length > 0 ? roleIds[0] : null
  showAssignRoleDialog.value = true
}

async function submitAssignRole() {
  if (!assigningMember.value) return
  submitting.value = true
  try {
    const roleIds = selectedRoleId.value !== null ? [selectedRoleId.value] : []
    const res = await sysUserApi.assignRoles({ user_id: assigningMember.value.id, role_ids: roleIds })
    if (res.success) {
      toast({ title: '角色分配成功', variant: 'success' })
      showAssignRoleDialog.value = false
    }
  } finally { submitting.value = false }
}

function confirmDeleteMember(user: SysUser) {
  deletingName.value = user.username
  deleteAction.value = async () => {
    const res = await sysUserApi.delete({ id: user.id })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      if (selectedDept.value) selectDept(selectedDept.value)
    }
  }
  showDeleteDialog.value = true
}

function openCreateOrgDialog() {
  editingOrg.value = null
  Object.assign(orgForm, { name: '', org_code: '', org_type: 'COMPANY', status: 1 })
  showOrgDialog.value = true
}

function openEditOrgDialog(org: SysOrg) {
  editingOrg.value = org
  Object.assign(orgForm, { name: org.name, org_code: org.org_code, org_type: org.org_type, status: org.status })
  showOrgDialog.value = true
}

async function submitOrgForm() {
  if (!orgForm.name.trim()) { toast({ title: '请输入组织名称', variant: 'destructive' }); return }
  submitting.value = true
  try {
    if (editingOrg.value) {
      const res = await sysOrgApi.update({ id: editingOrg.value.id, name: orgForm.name, org_type: orgForm.org_type, status: orgForm.status })
      if (res.success) {
        showOrgDialog.value = false
        loadOrgs()
        toast({ title: '更新成功', variant: 'success' })
      }
    } else {
      if (!orgForm.org_code.trim()) { toast({ title: '请输入机构码', variant: 'destructive' }); return }
      const res = await sysOrgApi.create({ name: orgForm.name, org_code: orgForm.org_code, org_type: orgForm.org_type })
      if (res.success) {
        showOrgDialog.value = false
        loadOrgs()
        createdAdminInfo.username = res.data?.admin_username || 'admin'
        createdAdminInfo.password = res.data?.admin_password || 'Admin@123'
        showOrgCreatedDialog.value = true
      }
    }
  } finally { submitting.value = false }
}

function confirmDeleteOrg(org: SysOrg) {
  deletingName.value = org.name
  deleteAction.value = async () => {
    const res = await sysOrgApi.delete({ id: org.id })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      if (selectedOrg.value?.id === org.id) { selectedOrg.value = null; deptList.value = [] }
      loadOrgs()
    }
  }
  showDeleteDialog.value = true
}

function openCreateDeptDialog(parentId: number) {
  editingDept.value = null
  Object.assign(deptForm, { dept_name: '', parent_id: parentId, sort: 0 })
  showDeptDialog.value = true
}

function openEditDeptDialog(dept: SysDept) {
  editingDept.value = dept
  Object.assign(deptForm, { dept_name: dept.dept_name, parent_id: dept.parent_id, sort: dept.sort })
  showDeptDialog.value = true
}

async function submitDeptForm() {
  if (!deptForm.dept_name.trim()) { toast({ title: '请输入部门名称', variant: 'destructive' }); return }
  if (!selectedOrg.value) return
  submitting.value = true
  try {
    let res
    if (editingDept.value) {
      res = await sysOrgApi.deptUpdate({ id: editingDept.value.id, dept_name: deptForm.dept_name, parent_id: deptForm.parent_id, sort: deptForm.sort })
    } else {
      res = await sysOrgApi.deptCreate({ org_id: selectedOrg.value.id, parent_id: deptForm.parent_id, dept_name: deptForm.dept_name, sort: deptForm.sort })
    }
    if (res.success) {
      toast({ title: editingDept.value ? '更新成功' : '创建成功', variant: 'success' })
      showDeptDialog.value = false
      loadDepts()
    }
  } finally { submitting.value = false }
}

function confirmDeleteDept(dept: SysDept) {
  deletingName.value = dept.dept_name
  deleteAction.value = async () => {
    const res = await sysOrgApi.deptDelete({ id: dept.id })
    if (res.success) {
      toast({ title: '删除成功', variant: 'success' })
      loadDepts()
    }
  }
  showDeleteDialog.value = true
}

async function confirmDelete() {
  if (!deleteAction.value) return
  submitting.value = true
  try { await deleteAction.value() } finally {
    submitting.value = false
    showDeleteDialog.value = false
  }
}

// API密钥管理函数
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

function maskApiKey(key: string): string {
  if (key.length <= 12) return key
  return key.substring(0, 12) + '...' + key.substring(key.length - 4)
}

function copyText(text: string) {
  navigator.clipboard.writeText(text).then(() => {
    toast({ title: '已复制到剪贴板', variant: 'success' })
  }).catch(() => {
    toast({ title: '复制失败', variant: 'destructive' })
  })
}

onMounted(() => {
  if (isSuperadmin) {
    loadOrgs()
  } else {
    loadAdminDepts()
  }
})
</script>

<style scoped>
.sys-container {
  height: calc(100vh - 44px);
  overflow: hidden;
}
.sys-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
