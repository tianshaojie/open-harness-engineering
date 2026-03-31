<!-- 通用数据表格组件 -->
<template>
  <div class="w-full h-full flex flex-col min-h-0 overflow-hidden">
    <!-- 搜索表单 -->
    <SearchForm
      :show="showSearch"
      :search-fields="searchFields"
      :initial-search-params="initialSearchParams"
      @search="handleSearch"
    />

    <!-- 表格内容（包含分页） -->
    <TableContent
      :columns="columns"
      :data="data"
      :loading="props.loading !== undefined ? props.loading : isLoading"
      :empty-title="emptyTitle"
      :empty-description="emptyDescription"
      :show-pagination="showPagination"
      :pagination-mode="paginationMode"
      :total="total"
      :current-page="currentPage"
      :page-size="pageSize"
      :page-size-options="pageSizeOptions"
      @page-change="(page) => emit('page-change', page)"
      @page-size-change="(size) => emit('page-size-change', size)"
      @rendered="emit('rendered')"
    >
      <!-- 传递插槽 -->
      <template v-for="(_, slotName) in $slots" :key="slotName" #[slotName]="slotProps">
        <slot :name="slotName" v-bind="slotProps" />
      </template>
    </TableContent>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import SearchForm from './SearchForm.vue';
import TableContent from './TableContent.vue';
import type { SearchField } from './SearchForm.vue';
import type { TableColumn, TableData } from './TableContent.vue';

// Props类型定义
interface Props {
  // 搜索相关
  showSearch?: boolean;
  searchFields?: SearchField[];
  initialSearchParams?: Record<string, any>;
  // 表格相关
  columns: TableColumn[];
  data: TableData[];
  // Loading 状态
  loading?: boolean;
  /** 无数据或加载失败时的标题 */
  emptyTitle?: string;
  /** 无数据或加载失败时的描述 */
  emptyDescription?: string;
  // 分页相关
  showPagination?: boolean;
  paginationMode?: 'server' | 'client';
  total?: number;
  currentPage?: number;
  pageSize?: number;
  pageSizeOptions?: number[];
}

// Props定义（使用 withDefaults 处理默认值）
const props = withDefaults(defineProps<Props>(), {
  showSearch: true,
  searchFields: () => [],
  initialSearchParams: () => ({}),
  data: () => [],
  emptyTitle: '暂无数据',
  emptyDescription: '',
  showPagination: true,
  paginationMode: 'server',
  total: 0,
  currentPage: 1,
  pageSize: 20,
  pageSizeOptions: () => [10, 20, 50, 100],
});

// Emits类型定义
interface Emits {
  (e: 'search', params: Record<string, any>): void;
  (e: 'page-change', page: number): void;
  (e: 'page-size-change', size: number): void;
  (e: 'rendered'): void;
}

// Emits定义
const emit = defineEmits<Emits>();

// Loading 状态
const isLoading = ref(false);

// 处理搜索事件
const handleSearch = (params: Record<string, any>) => {
  isLoading.value = true;
  emit('search', params);
};

// 监听数据变化，当数据更新时清除 loading
watch(
  () => props.data,
  (newData, oldData) => {
    // 只有在 loading 状态为 true 时才清除
    if (isLoading.value) {
      // 数据引用发生变化时，说明数据已更新，清除 loading
      if (newData !== oldData) {
        // 延迟清除 loading，确保过渡效果
        setTimeout(() => {
          isLoading.value = false;
        }, 100);
      }
    }
  },
  { immediate: false }
);
</script>
