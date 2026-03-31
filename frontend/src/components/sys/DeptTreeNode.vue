<template>
  <div class="dept-node">
    <div
      class="flex items-center gap-1.5 px-2 py-1.5 rounded-md hover:bg-[#F3F6FA] group cursor-pointer transition-colors"
      :class="selectedId === node.id ? 'bg-[#F3F6FA] text-[#1A2233] font-medium' : 'text-[#1A2233]'"
      :style="{ paddingLeft: `${depth * 16 + 8}px` }"
      @click="handleSelect"
    >
      <button
        v-if="node.children && node.children.length > 0"
        class="w-4 h-4 flex items-center justify-center text-muted-foreground flex-shrink-0"
        @click.stop="expanded = !expanded"
      >
        <ChevronRightIcon class="w-3 h-3 transition-transform" :class="expanded ? 'rotate-90' : ''" />
      </button>
      <span v-else class="w-4 h-4 flex items-center justify-center flex-shrink-0">
        <MinusIcon class="w-3 h-3 text-muted-foreground/40" />
      </span>
      <FolderOpenIcon v-if="selectedId === node.id" class="w-4 h-4 text-amber-500 flex-shrink-0" />
      <FolderIcon v-else class="w-4 h-4 text-amber-500 flex-shrink-0" />
      <span class="text-sm flex-1 truncate">{{ node.dept_name }}</span>
      <div class="hidden group-hover:flex items-center gap-0.5 flex-shrink-0">
        <Button variant="ghost" size="sm" class="h-6 w-6 p-0" @click.stop="$emit('add-child', node.id)">
          <PlusIcon class="w-3 h-3" />
        </Button>
        <Button variant="ghost" size="sm" class="h-6 w-6 p-0" @click.stop="$emit('edit', node)">
          <PencilIcon class="w-3 h-3" />
        </Button>
        <Button variant="ghost" size="sm" class="h-6 w-6 p-0 text-destructive hover:text-destructive" @click.stop="$emit('delete', node)">
          <Trash2Icon class="w-3 h-3" />
        </Button>
      </div>
    </div>
    <template v-if="expanded && node.children && node.children.length > 0">
      <DeptTreeNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :depth="depth + 1"
        :selected-id="selectedId"
        @add-child="$emit('add-child', $event)"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @select="$emit('select', $event)"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { ChevronRightIcon, MinusIcon, FolderIcon, FolderOpenIcon, PlusIcon, PencilIcon, Trash2Icon } from 'lucide-vue-next'

interface DeptNode {
  id: number
  org_id: number
  parent_id: number
  dept_name: string
  sort: number
  create_time: string | null
  children?: DeptNode[]
}

const props = withDefaults(defineProps<{
  node: DeptNode
  depth?: number
  selectedId?: number | null
}>(), { depth: 0, selectedId: null })

const emit = defineEmits<{
  'add-child': [parentId: number]
  'edit': [dept: DeptNode]
  'delete': [dept: DeptNode]
  'select': [dept: DeptNode]
}>()

const expanded = ref(true)

function handleSelect() {
  emit('select', props.node)
}
</script>
