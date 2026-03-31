<template>
  <div>
    <label
      class="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-muted/50 cursor-pointer"
      :style="{ paddingLeft: `${depth * 16 + 8}px` }"
    >
      <input
        type="checkbox"
        :checked="selectedIds.includes(node.id)"
        @change="$emit('toggle', node.id)"
        class="rounded"
      />
      <component :is="typeIcon" class="w-3.5 h-3.5 flex-shrink-0" :class="typeIconClass" />
      <span class="text-sm">{{ node.name }}</span>
      <span class="text-xs text-muted-foreground font-mono ml-1">{{ node.perm_code || '' }}</span>
    </label>
    <template v-if="node.children && node.children.length > 0">
      <ResourceCheckNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :depth="depth + 1"
        :selected-ids="selectedIds"
        @toggle="$emit('toggle', $event)"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FolderIcon, MenuIcon, MousePointerClickIcon } from 'lucide-vue-next'

interface ResourceNode {
  id: number
  pid: number
  name: string
  type: number
  perm_code: string | null
  children?: ResourceNode[]
}

const props = withDefaults(defineProps<{
  node: ResourceNode
  depth?: number
  selectedIds: number[]
}>(), { depth: 0 })

defineEmits<{ 'toggle': [id: number] }>()

const typeIcon = computed(() => {
  const map: Record<number, any> = { 1: FolderIcon, 2: MenuIcon, 3: MousePointerClickIcon }
  return map[props.node.type] || MenuIcon
})

const typeIconClass = computed(() => {
  const map: Record<number, string> = {
    1: 'text-blue-500', 2: 'text-green-500', 3: 'text-orange-500'
  }
  return map[props.node.type] || 'text-gray-400'
})
</script>
