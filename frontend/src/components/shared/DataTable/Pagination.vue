<template>
  <div class="px-4 py-3 bg-white border-t border-gray-200">
    <div class="flex items-center justify-between gap-4">
      <!-- 每页条数和总条数 -->
      <div class="flex items-center gap-2">
        <Select
          :model-value="pageSize.toString()"
          @update:model-value="handlePageSizeChange"
        >
          <SelectTrigger class="h-8 w-[100px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem
              v-for="size in pageSizeOptions"
              :key="size"
              :value="size.toString()"
            >
              {{ size }}条/页
            </SelectItem>
          </SelectContent>
        </Select>
        <span class="text-sm text-gray-600">共 {{ total }} 条</span>
      </div>
      
      <!-- 分页按钮 -->
      <div class="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          :disabled="currentPage <= 1"
          @click="handlePageChange(1)"
        >
          首页
        </Button>
        <Button
          variant="outline"
          size="sm"
          :disabled="currentPage <= 1"
          @click="handlePageChange(currentPage - 1)"
        >
          上一页
        </Button>
        <span class="text-sm text-gray-600">
          第 {{ currentPage }} / {{ totalPages }} 页
        </span>
        <Button
          variant="outline"
          size="sm"
          :disabled="currentPage >= totalPages"
          @click="handlePageChange(currentPage + 1)"
        >
          下一页
        </Button>
        <Button
          variant="outline"
          size="sm"
          :disabled="currentPage >= totalPages"
          @click="handlePageChange(totalPages)"
        >
          尾页
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface Props {
  total: number
  currentPage: number
  totalPages: number
  pageSize: number
  pageSizeOptions: number[]
}

defineProps<Props>()

const emit = defineEmits<{
  'page-change': [page: number]
  'page-size-change': [size: number]
}>()

const handlePageChange = (page: number) => {
  emit('page-change', page)
}

const handlePageSizeChange = (value: string) => {
  emit('page-size-change', parseInt(value, 10))
}
</script>
