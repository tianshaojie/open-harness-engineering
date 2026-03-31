<template>
  <!-- 🔧 修复：当有列定义时，即使数据为空数组也显示表格 -->
  <!-- 当有数据或列定义时显示表格 -->
  <div v-if="hasTableData || hasColumns" :class="studioMode ? 'flex flex-col h-full' : 'flex flex-col'">
    <!-- 数据统计栏：仅在非历史消息时显示（通过 currentLimit 判断） -->
    <div v-if="shouldShowStatsBar" class="mb-3 px-4 py-2 bg-gray-50 border rounded-lg flex items-center gap-4 text-sm flex-nowrap flex-shrink-0">
      <div class="flex items-center gap-2">
        <label for="limit-select-chat" class="text-gray-600">SQL 查询条数：</label>
        <Select
          :model-value="selectedLimit"
          @update:model-value="(val) => {
            const normalized = normalizeLimitValue(val);
            if (typeof normalized === 'number') {
              selectedLimit.value = normalized;
              emit('limitChange', normalized);
            }
          }"
        >
          <SelectTrigger
            id="limit-select-chat"
            class="w-[110px] h-8 text-xs"
          >
            <SelectValue>
              {{ selectedLimit }} 条
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectItem
              v-for="option in availableLimitOptions"
              :key="option"
              :value="option"
              class="text-xs whitespace-nowrap"
            >
              {{ option }} 条
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
      <span v-if="hasTotalCount" class="text-gray-700">
        数据总数：<span class="font-semibold text-gray-900">{{ displayTotalCount }}</span> 条
      </span>
      <span :class="loadedCountClass">
        已加载 {{ loadedCount }} 条
      </span>
      <span v-if="shouldShowLimitTip" class="text-xs text-amber-600 truncate min-w-0 flex-1">
        SQL 已包含行数限制（当前 {{ selectedLimit }}），修改条数会重写 SQL 并重新执行
      </span>
    </div>

    <!-- 表格容器：限制高度，让 DataTable 内部处理滚动，分页固定在底部 -->
    <div :class="['relative', studioMode ? 'flex-1 min-h-0' : '', tableWrapperClasses]">
      <DataTable
        :data="tableData"
        :columns="tableColumns"
        :pagination-mode="'client'"
        :show-search="false"
        :show-pagination="true"
        :page-size="20"
        :page-size-options="[5, 10, 20, 50, 100]"
        @rendered="handleTableRendered"
      />

      <!-- 加载蒙版：数据刷新时显示 -->
      <div v-if="isRefreshing" class="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
        <Loading type="spinner" text="数据加载中..." />
      </div>
    </div>
  </div>
  <!-- 当有错误信息且不在刷新时显示错误提示 -->
  <div v-else-if="dataErrorMessage && !isRefreshing" class="h-full flex flex-col">
    <div class="flex items-start justify-center h-full p-6 overflow-auto">
      <div class="error-message w-full max-w-full">
        <span class="break-words whitespace-pre-wrap">{{ dataErrorMessage }}</span>
      </div>
    </div>
  </div>
  <!-- 无数据或错误信息时显示空状态或加载状态 -->
  <div v-else class="h-full flex flex-col">
    <div class="flex items-center justify-center h-full">
      <EmptyState :loading="isRefreshing" loading-text="数据加载中..." title="暂无数据" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import DataTable from '@/components/DataTable/index.vue';
import EmptyState from '@/components/EmptyState/index.vue';
import Loading from '@/components/Loading/index.vue';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface Props {
  userData: any[] | null;
  columns?: string[] | null;
  dataErrorMessage?: string | null; // 添加数据错误信息字段
  studioMode?: boolean; // 是否在studio模式下使用，限制表格高度
  maxHeight?: string; // 最大高度值，用于精确控制
  totalCount?: number; // 数据总数（通过COUNT查询获取）
  currentLimit?: number; // 当前的limit值
  limitSource?: string | null; // limit来源
  isRefreshing?: boolean; // 是否正在刷新SQL数据
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'rendered'): void;
  (e: 'table-rendered'): void;
  (e: 'limitChange', limit: number): void;
}>();

// SQL查询条数限制
const normalizeLimitValue = (value: unknown) => {
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric <= 0) {
    return undefined;
  }
  return Math.trunc(numeric);
};

const selectedLimit = ref(normalizeLimitValue(props.currentLimit) ?? 1000);

// 监听props.currentLimit变化，同步更新selectedLimit
watch(() => props.currentLimit, (newLimit) => {
  const normalized = normalizeLimitValue(newLimit);
  if (typeof normalized === 'number') {
    selectedLimit.value = normalized;
  }
});

// 判断是否应该显示统计栏（仅在非历史消息时显示）
const shouldShowStatsBar = computed(() => {
  return props.currentLimit !== undefined && props.currentLimit !== null;
});

const loadedCount = computed(() => tableData.value.length);

// 展示用总数（仅在后端返回 COUNT 结果时展示）
const hasTotalCount = computed(() => {
  return typeof props.totalCount === 'number';
});

const displayTotalCount = computed(() => {
  return props.totalCount ?? 0;
});

const loadedCountClass = computed(() => {
  if (typeof props.totalCount === 'number' && loadedCount.value < props.totalCount) {
    return 'text-green-600';
  }
  return 'text-gray-600';
});

// 根据总数动态计算可用的limit选项
const availableLimitOptions = computed(() => {
  const options = [1000, 5000, 10000];

  if (!options.includes(selectedLimit.value)) {
    options.push(selectedLimit.value);
  }

  return options.sort((a, b) => a - b);
});

const shouldShowLimitTip = computed(() => {
  return props.limitSource === 'llm' && typeof selectedLimit.value === 'number';
});

// 处理limit变化（保留：用于兼容历史代码/阅读）
const handleLimitChange = () => {
  emit('limitChange', selectedLimit.value);
};

// containerClasses 已移除，不再需要

// 🔧 修复：判断是否有表格数据（数据不为null且长度大于0）
const hasTableData = computed(() => {
  return props.userData !== null && props.userData !== undefined && Array.isArray(props.userData) && props.userData.length > 0;
});

// 🔧 修复：判断是否有列定义
const hasColumns = computed(() => {
  return props.columns !== null && props.columns !== undefined && Array.isArray(props.columns) && props.columns.length > 0;
});

// 计算表格容器样式类（用于表格包装器，限制高度，让 DataTable 内部处理滚动）
const tableWrapperClasses = computed(() => {
  const classes = [];
  
  // 在 studio 模式下，继承父容器高度，不设置最大高度限制
  if (props.studioMode) {
    classes.push('h-full');
  } else if (props.maxHeight) {
    // 非 studio 模式下，如果有 maxHeight，设置固定高度（不是 max-height，而是 height）
    classes.push(`h-[${props.maxHeight}]`);
  } else {
    // 默认高度 400px，与图表和 SQL 保持一致
    classes.push('h-[400px]');
  }
  
  // 确保容器是 flex 布局，让 DataTable 可以占据全部高度
  classes.push('flex', 'flex-col');
  
  return classes.join(' ');
});

// 转换数据格式，确保每条数据都有 id 字段
const tableData = computed(() => {
  if (!props.userData || props.userData.length === 0) return [];
  return props.userData.map((item, index) => ({
    ...item,
    id: item.id || index
  }));
});

// 计算合适的列宽
const calculateColumnWidth = (columnCount: number): string | undefined => {
  if (columnCount === 0) return undefined;
  
  if (columnCount === 1) {
    return '100%';
  } else if (columnCount === 2) {
    return '50%';
  } else if (columnCount === 3) {
    return '33.33%';
  } else if (columnCount === 4) {
    return '25%';
  } else if (columnCount <= 6) {
    const percent = (100 / columnCount).toFixed(2);
    return `${percent}%`;
  } else {
    return '140px';
  }
};

// 转换列定义为 DataTable 需要的格式，并计算列宽
const tableColumns = computed(() => {
  let columns: Array<{ key: string; title: string; width?: string }> = [];
  
  // 如果提供了列定义
  const columnNames = props.columns || [];
  if (columnNames.length > 0) {
    columns = columnNames.map(col => ({
      key: col,
      title: col
    }));
  } else if (props.userData && props.userData.length > 0) {
    // 如果没有提供列定义，从第一条数据中提取
    const firstItem = props.userData[0];
    const keys = Object.keys(firstItem);
    columns = keys.map(key => ({
      key: key,
      title: key
    }));
  }
  
  // 如果没有设置列宽，自动计算（统一处理，不区分 studioMode）
  if (columns.length > 0) {
    const columnWidth = calculateColumnWidth(columns.length);
    if (columnWidth) {
      columns = columns.map(col => ({
        ...col,
        width: col.width || columnWidth
      }));
    }
  }
  
  return columns;
});

// 监听数据变化
watch(() => props.userData, (newData: any[] | null) => {
  // 数据更新时的处理逻辑可以在这里添加
}, { deep: true });

// 监听列定义变化
watch(
  () => props.columns, 
  (newColumns) => {
    // 列定义更新时的处理逻辑可以在这里添加
  }, 
  { deep: true }
);

// 监听错误信息变化
watch(
  () => props.dataErrorMessage,
  (newErrorMessage) => {
    if (newErrorMessage) {
      // 错误信息更新时的处理逻辑可以在这里添加
    }
  }
);

// 处理表格渲染完成事件
const handleTableRendered = () => {
  emit('rendered');
  emit('table-rendered');
};
</script>

<style scoped>
.error-message {
  display: flex;
  align-items: flex-start;
  color: #d54941;
  font-size: 14px;
  padding: 8px 12px;
  background-color: rgba(213, 73, 65, 0.1);
  border-radius: 4px;
  margin-top: 8px;
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  min-width: 0;
  max-width: 100%;
}

.error-message span {
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
}

@media screen and (max-width: 768px) {
  .error-message {
    font-size: 12px !important;
    padding: 6px 8px !important;
  }
}
</style> 
