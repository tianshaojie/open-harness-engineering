<template>
  <div class="w-full bg-white rounded-lg border border-gray-200 p-4 mb-4">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="field in searchFields"
        :key="field.key"
        class="flex items-center gap-2"
      >
        <label class="text-sm font-medium text-gray-700 whitespace-nowrap">
          {{ field.label }}:
        </label>
        
        <!-- Input 输入框 -->
        <Input
          v-if="field.type === 'input'"
          :model-value="searchForm[field.key] as string"
          :placeholder="field.placeholder || '请输入'"
          class="flex-1"
          @update:model-value="(val) => updateField(field.key, val)"
        />
        
        <!-- Select 选择器 -->
        <Select
          v-else-if="field.type === 'select'"
          :model-value="searchForm[field.key] as string"
          @update:model-value="(val) => updateField(field.key, val)"
        >
          <SelectTrigger class="flex-1">
            <SelectValue :placeholder="field.placeholder || '请选择'" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem
              v-for="option in field.options"
              :key="option.value"
              :value="String(option.value)"
            >
              {{ option.label }}
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      <!-- 操作按钮 -->
      <div class="flex gap-2 md:col-span-3">
        <Button @click="$emit('search')">
          查询
        </Button>
        <Button variant="outline" @click="$emit('reset')">
          重置
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import type { SearchField } from './index.vue'

interface Props {
  searchFields: SearchField[]
  searchForm: Record<string, unknown>
}

const props = defineProps<Props>()

const emit = defineEmits<{
  search: []
  reset: []
  'update:searchForm': [value: Record<string, unknown>]
}>()

const updateField = (key: string, value: unknown) => {
  const newForm = { ...props.searchForm, [key]: value }
  emit('update:searchForm', newForm)
}
</script>
