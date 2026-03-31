<template>
  <tr class="border-b border-border/50 hover:bg-muted/30 transition-colors">
    <td class="px-4 py-1.5">
      <div class="flex items-center gap-1" :style="{ paddingLeft: `${depth * 20}px` }">
        <button
          v-if="node.children && node.children.length > 0"
          class="w-4 h-4 flex items-center justify-center text-muted-foreground flex-shrink-0"
          @click="expanded = !expanded"
        >
          <ChevronRightIcon class="w-3 h-3 transition-transform" :class="expanded ? 'rotate-90' : ''" />
        </button>
        <span v-else class="w-4 h-4 flex-shrink-0" />
        <component :is="typeIcon" class="w-4 h-4 flex-shrink-0" :class="typeIconClass" />
        <span class="text-sm">{{ node.name }}</span>
      </div>
    </td>
    <td class="px-4 py-1.5">
      <span class="text-xs px-1.5 py-0.5 rounded" :class="typeBadgeClass">{{ typeLabel }}</span>
    </td>
    <td class="px-4 py-1.5 text-xs text-muted-foreground font-mono">{{ node.perm_code || '-' }}</td>
    <td class="px-4 py-1.5 text-xs text-muted-foreground">{{ node.path || '-' }}</td>
    <td class="px-4 py-1.5 text-sm text-center">{{ node.sort }}</td>
    <td class="px-4 py-1.5 text-center">
      <span class="text-xs" :class="node.visible === 1 ? 'text-green-600' : 'text-gray-400'">
        {{ node.visible === 1 ? '是' : '否' }}
      </span>
    </td>
    <td class="px-4 py-1.5">
      <div class="flex items-center justify-center gap-1">
        <Button variant="ghost" size="sm" class="h-7 px-2 text-xs" @click="$emit('add-child', node.id)">
          子菜单
        </Button>
        <Button variant="ghost" size="sm" class="h-7 px-2 text-xs" @click="$emit('edit', node)">
          编辑
        </Button>
        <Button variant="ghost" size="sm" class="h-7 px-2 text-xs text-destructive hover:text-destructive" @click="$emit('delete', node)">
          删除
        </Button>
      </div>
    </td>
  </tr>
  <template v-if="expanded && node.children && node.children.length > 0">
    <ResourceTreeRow
      v-for="child in node.children"
      :key="child.id"
      :node="child"
      :depth="depth + 1"
      @add-child="$emit('add-child', $event)"
      @edit="$emit('edit', $event)"
      @delete="$emit('delete', $event)"
    />
  </template>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Button } from '@/components/ui/button'
import { ChevronRightIcon, FolderIcon, MenuIcon, MousePointerClickIcon, BotIcon } from 'lucide-vue-next'

interface ResourceNode {
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
  children?: ResourceNode[]
}

const props = withDefaults(defineProps<{
  node: ResourceNode
  depth?: number
}>(), { depth: 0 })

defineEmits<{
  'add-child': [pid: number]
  'edit': [item: ResourceNode]
  'delete': [item: ResourceNode]
}>()

const expanded = ref(true)

const typeLabel = computed(() => {
  const map: Record<number, string> = { 1: '目录', 2: '菜单', 3: '按钮', 4: 'AI智能体' }
  return map[props.node.type] || '未知'
})

const typeBadgeClass = computed(() => {
  const map: Record<number, string> = {
    1: 'bg-blue-100 text-blue-700',
    2: 'bg-green-100 text-green-700',
    3: 'bg-orange-100 text-orange-700',
    4: 'bg-purple-100 text-purple-700'
  }
  return map[props.node.type] || 'bg-gray-100 text-gray-600'
})

const typeIcon = computed(() => {
  const map: Record<number, any> = { 1: FolderIcon, 2: MenuIcon, 3: MousePointerClickIcon, 4: BotIcon }
  return map[props.node.type] || MenuIcon
})

const typeIconClass = computed(() => {
  const map: Record<number, string> = {
    1: 'text-blue-500',
    2: 'text-green-500',
    3: 'text-orange-500',
    4: 'text-purple-500'
  }
  return map[props.node.type] || 'text-gray-400'
})
</script>
