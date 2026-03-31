<template>
  <div class="bg-white rounded-lg border border-gray-200 overflow-hidden h-full flex flex-col">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-gray-500">加载中...</div>
    </div>
    
    <!-- 空数据 -->
    <div v-else-if="data.length === 0" class="flex-1 flex items-center justify-center">
      <div class="text-gray-500">暂无数据</div>
    </div>
    
    <!-- 表格内容 -->
    <div v-else class="overflow-auto flex-1">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead
              v-for="col in columns"
              :key="col.key"
              :style="col.width ? { width: col.width + 'px' } : {}"
            >
              {{ col.title }}
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(row, index) in data" :key="index">
            <TableCell
              v-for="col in columns"
              :key="col.key"
            >
              <!-- 插槽列 -->
              <slot
                v-if="col.slot"
                :name="col.slot"
                :row="row"
                :value="row[col.key]"
                :index="index"
              />
              <!-- 自定义渲染 -->
              <!-- eslint-disable-next-line vue/no-v-html -->
              <div
                v-else-if="col.render"
                v-html="col.render(row[col.key], row)"
              />
              <!-- 默认显示 -->
              <span v-else>{{ String(row[col.key] ?? '') }}</span>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import type { Column } from './index.vue'

interface Props {
  columns: Column[]
  data: Record<string, unknown>[]
  loading?: boolean
}

defineProps<Props>()
</script>
