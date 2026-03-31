<template>
  <div class="data-table-container flex flex-col h-full">
    <!-- 搜索表单 -->
    <SearchForm
      v-if="searchFields && searchFields.length > 0"
      :search-fields="searchFields"
      :search-form="searchForm"
      @search="handleSearch"
      @reset="handleReset"
    />
    
    <!-- 表格内容 -->
    <div class="flex-1 min-h-0 overflow-hidden">
      <TableContent
        :columns="columns"
        :data="data"
        :loading="loading"
      />
    </div>
    
    <!-- 分页 -->
    <Pagination
      v-if="pagination"
      :total="pagination.total"
      :current-page="pagination.page"
      :page-size="pagination.size"
      :total-pages="Math.ceil(pagination.total / pagination.size)"
      :page-size-options="[10, 20, 50, 100]"
      @page-change="handlePageChange"
      @page-size-change="handlePageSizeChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import SearchForm from './SearchForm.vue'
import TableContent from './TableContent.vue'
import Pagination from './Pagination.vue'

export interface SearchField {
  key: string
  label: string
  type: 'input' | 'select'
  placeholder?: string
  options?: Array<{ label: string; value: string | number }>
}

export interface Column {
  key: string
  title: string
  width?: number
  slot?: string
  render?: (value: unknown, row: Record<string, unknown>) => string
}

export interface PaginationData {
  total: number
  page: number
  size: number
}

interface Props {
  searchFields?: SearchField[]
  columns: Column[]
  data: Record<string, unknown>[]
  loading?: boolean
  pagination?: PaginationData
}

const props = defineProps<Props>()

const emit = defineEmits<{
  search: [params: Record<string, unknown>]
  'page-change': [page: number]
  'page-size-change': [size: number]
}>()

const searchForm = ref<Record<string, unknown>>({})

// 初始化搜索表单
watch(
  () => props.searchFields,
  (fields) => {
    if (fields) {
      const form: Record<string, unknown> = {}
      fields.forEach((field) => {
        form[field.key] = ''
      })
      searchForm.value = form
    }
  },
  { immediate: true }
)

const handleSearch = () => {
  emit('search', { ...searchForm.value })
}

const handleReset = () => {
  if (props.searchFields) {
    props.searchFields.forEach((field) => {
      searchForm.value[field.key] = ''
    })
  }
  emit('search', {})
}

const handlePageChange = (page: number) => {
  emit('page-change', page)
}

const handlePageSizeChange = (size: number) => {
  emit('page-size-change', size)
}
</script>

<style scoped>
.data-table-container {
  background: #f9fafb;
}
</style>
