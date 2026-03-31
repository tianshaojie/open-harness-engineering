<template>
  <div class="px-4 md:px-2 py-3 md:py-1.5 md:py-2 bg-white sticky bottom-0 z-[5]">
    <!-- 移动端单行均匀排列 -->
    <div class="md:hidden flex items-center justify-between gap-2">
      <!-- 每页条数和总条数 -->
      <div class="flex items-center gap-2 shrink-0">
        <Select
          :model-value="pageSize.toString()"
          @update:model-value="handlePageSizeChange"
        >
          <SelectTrigger class="h-7 !w-auto min-w-[70px] border border-gray-300 rounded px-1.5 py-[2px] bg-white text-gray-600 text-xs cursor-pointer">
            <SelectValue :placeholder="pageSize + '条/页'" />
          </SelectTrigger>
          <SelectContent class="z-[10000] !w-auto min-w-[var(--radix-select-trigger-width)]">
            <SelectItem
              v-for="size in pageSizeOptions"
              :key="size"
              :value="size.toString()"
              class="whitespace-nowrap text-xs"
            >
              {{ size }}条/页
            </SelectItem>
          </SelectContent>
        </Select>
        <span class="text-gray-600 text-xs whitespace-nowrap">共 {{ total }} 条</span>
      </div>
      <!-- 分页按钮和页码 -->
      <div class="flex items-center gap-1 shrink-0">
        <Button
          v-for="btn in leftButtons"
          :key="btn.key"
          variant="outline"
          size="icon"
          :class="`min-w-8 h-8 p-0 flex items-center justify-center text-xs border border-gray-300 rounded bg-white disabled:cursor-not-allowed disabled:text-gray-300 disabled:bg-gray-50 ${btn.key === 'first' ? 'hidden' : ''}`"
          :disabled="btn.disabled"
          :aria-label="btn.ariaLabel"
          @click="handlePageChange(btn.action)"
        >
          {{ btn.label }}
        </Button>
        <div class="min-w-[60px] text-center">
          <span class="text-gray-600 text-xs whitespace-nowrap">{{ currentPage }} / {{ totalPages }}</span>
        </div>
        <Button
          v-for="btn in rightButtons"
          :key="btn.key"
          variant="outline"
          size="icon"
          :class="`min-w-8 h-8 p-0 flex items-center justify-center text-xs border border-gray-300 rounded bg-white disabled:cursor-not-allowed disabled:text-gray-300 disabled:bg-gray-50 ${btn.key === 'last' ? 'hidden' : ''}`"
          :disabled="btn.disabled"
          :aria-label="btn.ariaLabel"
          @click="handlePageChange(btn.action)"
        >
          {{ btn.label }}
        </Button>
      </div>
    </div>
    
    <!-- PC端原有布局 -->
    <div class="hidden md:flex flex-wrap items-center justify-between gap-1.5 md:gap-2">
      <!-- 每页条数和总条数 -->
      <div class="flex items-center gap-1.5 md:gap-2 shrink-0">
        <Select
          :model-value="pageSize.toString()"
          @update:model-value="handlePageSizeChange"
        >
          <SelectTrigger class="h-7 md:h-7 !w-auto min-w-[60px] md:min-w-[70px] border border-gray-300 rounded px-1 md:px-1.5 py-[2px] bg-white text-gray-600 text-[11px] md:text-xs cursor-pointer shrink-0">
            <SelectValue :placeholder="pageSize + '条/页'" />
          </SelectTrigger>
          <SelectContent class="z-[10000] !w-auto min-w-[var(--radix-select-trigger-width)]">
            <SelectItem
              v-for="size in pageSizeOptions"
              :key="size"
              :value="size.toString()"
              class="whitespace-nowrap text-xs"
            >
              {{ size }}条/页
            </SelectItem>
          </SelectContent>
        </Select>
        <span class="text-gray-600 text-[11px] md:text-xs whitespace-nowrap shrink-0">共 {{ total }} 条</span>
      </div>
      <!-- 分页按钮和页码 -->
      <div class="flex items-center gap-1 md:gap-1.5 shrink-0">
        <!-- 首页按钮：宽度足够时显示 -->
        <Button
          v-for="btn in leftButtons"
          :key="btn.key"
          variant="outline"
          size="icon"
          :class="`min-w-6 h-6 md:min-w-7 md:h-7 p-0 flex items-center justify-center text-[11px] md:text-xs border border-gray-300 rounded bg-white disabled:cursor-not-allowed disabled:text-gray-300 disabled:bg-gray-50 ${btn.key === 'first' ? 'hidden xl:flex' : ''}`"
          :disabled="btn.disabled"
          :aria-label="btn.ariaLabel"
          @click="handlePageChange(btn.action)"
        >
          {{ btn.label }}
        </Button>
        <div class="min-w-[60px] md:min-w-[80px] text-center shrink-0">
          <span class="text-gray-600 text-[11px] md:text-xs whitespace-nowrap">
            <span class="hidden lg:inline">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
            <span class="lg:hidden">{{ currentPage }} / {{ totalPages }}</span>
          </span>
        </div>
        <!-- 下一页/尾页按钮：尾页按钮在宽度足够时显示 -->
        <Button
          v-for="btn in rightButtons"
          :key="btn.key"
          variant="outline"
          size="icon"
          :class="`min-w-6 h-6 md:min-w-7 md:h-7 p-0 flex items-center justify-center text-[11px] md:text-xs border border-gray-300 rounded bg-white disabled:cursor-not-allowed disabled:text-gray-300 disabled:bg-gray-50 ${btn.key === 'last' ? 'hidden xl:flex' : ''}`"
          :disabled="btn.disabled"
          :aria-label="btn.ariaLabel"
          @click="handlePageChange(btn.action)"
        >
          {{ btn.label }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface Props {
  total: number;
  currentPage: number;
  totalPages: number;
  pageSize: number;
  pageSizeOptions: number[];
}

const props = defineProps<Props>();

const emit = defineEmits<{
  'page-change': [page: number];
  'page-size-change': [size: number];
}>();


// 左侧按钮配置（首页、上一页）
const leftButtons = computed(() => [
  {
    key: 'first',
    label: '«',
    action: 1,
    disabled: props.currentPage <= 1,
    ariaLabel: '首页',
  },
  {
    key: 'prev',
    label: '‹',
    action: props.currentPage - 1,
    disabled: props.currentPage <= 1,
    ariaLabel: '上一页',
  },
]);

// 右侧按钮配置（下一页、尾页）
const rightButtons = computed(() => [
  {
    key: 'next',
    label: '›',
    action: props.currentPage + 1,
    disabled: props.currentPage >= props.totalPages,
    ariaLabel: '下一页',
  },
  {
    key: 'last',
    label: '»',
    action: props.totalPages,
    disabled: props.currentPage >= props.totalPages,
    ariaLabel: '尾页',
  },
]);

// 分页切换
const handlePageChange = (page: number) => {
  if (page < 1 || page > props.totalPages) return;
  emit('page-change', page);
};

// 每页条数变化
const handlePageSizeChange = (value: string | number) => {
  const newSize = typeof value === 'string' ? parseInt(value, 10) : value;
  emit('page-size-change', newSize);
};
</script>

<style scoped>
/* 确保 Select 下拉菜单在分享页面等高 z-index 环境下正常显示 */
:deep([data-radix-select-content]) {
  z-index: 10000 !important;
}

:deep([data-radix-popper-content-wrapper]) {
  z-index: 10000 !important;
}

/* 确保下拉选项文本不换行 */
:deep([data-radix-select-item]) {
  white-space: nowrap !important;
}

:deep([data-radix-select-item-text]) {
  white-space: nowrap !important;
}

/* 让下拉菜单宽度根据内容自适应（根据选项中最长的文本） */
:deep([data-radix-select-content]) {
  width: max-content !important;
  min-width: var(--radix-select-trigger-width) !important;
}
</style>

