<template>
  <div v-if="show" class="w-full relative z-10 bg-white rounded-lg border border-gray-200 p-3 mb-5" style="font-size: clamp(0.75rem, 2vw, 0.875rem);">
    <div class="search-form-grid">
      <div 
        v-for="field in searchFields" 
        :key="field.key" 
        :class="[
          'search-form-item',
          field.type === 'dateRange' ? 'search-form-item-date-range' : 'search-form-item-normal'
        ]"
      >
        <!-- 空数据占位，只占据宽度不显示内容 -->
        <div v-if="!field.label" class="w-full h-9 flex-1 md:block hidden"></div>
        <!-- 正常搜索字段 -->
        <div v-else class="flex items-center gap-2 w-full min-w-0">
          <label class="text-sm md:text-sm font-medium text-gray-500 whitespace-nowrap shrink-0" style="font-size: 1em;">{{ field.label }}:</label>
          <!-- Select 选择器 -->
          <template v-if="field.type === 'select'">
            <Select v-model="searchForm[field.key]">
              <SelectTrigger class="h-9 flex-1 min-w-0 max-w-[220px]">
                <SelectValue :placeholder="field.placeholder || '全部'" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="option in (field.options || []).filter(opt => opt.value !== '')"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </SelectItem>
              </SelectContent>
            </Select>
          </template>
          <!-- Input 输入框 -->
          <template v-else-if="field.type === 'input'">
            <Input
              v-model="searchForm[field.key]"
              :placeholder="field.placeholder"
              class="h-9 flex-1 min-w-0 max-w-[220px]"
            />
          </template>
          <!-- DateRange 日期范围 -->
          <template v-else-if="field.type === 'dateRange' && field.startKey && field.endKey">
            <div class="date-range-container">
              <div class="date-picker-wrapper">
                <DatePicker
                  :model-value="searchForm[field.startKey]"
                  :placeholder="field.startPlaceholder || '开始日期'"
                  :selected-date="startDate"
                  @update:model-value="handleStartDateChange(field.startKey, $event)"
                  @open="handleStartCalendarOpen"
                />
              </div>
              <span class="date-range-separator">至</span>
              <div class="date-picker-wrapper">
                <DatePicker
                  :model-value="searchForm[field.endKey]"
                  :placeholder="field.endPlaceholder || '结束日期'"
                  :selected-date="endDate"
                  @update:model-value="handleEndDateChange(field.endKey, $event)"
                  @open="handleEndCalendarOpen"
                />
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="search-form-actions">
        <div class="flex gap-3">
          <Button variant="default" class="h-9 px-4 whitespace-nowrap" @click="handleSearch">
            <Search class="h-4 w-4 mr-2" />
            查询
          </Button>
          <Button variant="secondary" class="h-9 px-4 whitespace-nowrap" @click="handleReset">
            <RotateCcw class="h-4 w-4 mr-2" />
            重置
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { Search, RotateCcw } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import DatePicker from './DatePicker.vue';

// 搜索字段类型定义
export interface SearchField {
  key: string;
  label: string;
  type: 'input' | 'select' | 'dateRange';
  placeholder?: string;
  options?: Array<{ label: string; value: any }>;
  startKey?: string;
  endKey?: string;
  startPlaceholder?: string;
  endPlaceholder?: string;
}

interface Props {
  show?: boolean;
  searchFields: SearchField[];
  initialSearchParams?: Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
  show: true,
  searchFields: () => [],
  initialSearchParams: () => ({}),
});

const emit = defineEmits<{
  search: [params: Record<string, any>];
}>();

interface SearchFormData {
  [key: string]: any;
}

// 搜索表单数据
const searchForm = ref<SearchFormData>({ ...props.initialSearchParams });

// 日期范围选择器状态
const startDate = ref<Date | undefined>(undefined);
const endDate = ref<Date | undefined>(undefined);
const showEndCalendar = ref(false);
const showStartCalendar = ref(false);

// 监听初始搜索参数变化
watch(
  () => props.initialSearchParams,
  (newVal, oldVal) => {
    if (newVal !== oldVal && newVal) {
      searchForm.value = { ...newVal };
    }
  },
  { immediate: true }
);

// 解析日期字符串为 Date 对象
const parseDate = (dateString: string): Date | undefined => {
  if (!dateString) return undefined;
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? undefined : date;
};

// 处理开始日期变化
const handleStartDateChange = (key: string, value: string) => {
  searchForm.value[key] = value;
  startDate.value = parseDate(value);
};

// 处理结束日期变化
const handleEndDateChange = (key: string, value: string) => {
  searchForm.value[key] = value;
  endDate.value = parseDate(value);
};

// 处理开始日历打开
const handleStartCalendarOpen = () => {
  showEndCalendar.value = false;
};

// 处理结束日历打开
const handleEndCalendarOpen = () => {
  showStartCalendar.value = false;
};

// 搜索处理
const handleSearch = () => {
  const params = { ...searchForm.value };
  // 处理select的全部选项
  Object.keys(params).forEach(key => {
    if (params[key] === 'all') {
      params[key] = '';
    }
  });
  emit('search', params);
};

// 重置处理（重置后自动触发搜索）
const handleReset = () => {
  const resetForm: SearchFormData = {};
  props.searchFields.forEach(field => {
    if (field.type === 'select') {
      resetForm[field.key] = 'all';
    } else if (field.type === 'dateRange' && field.startKey && field.endKey) {
      resetForm[field.startKey] = '';
      resetForm[field.endKey] = '';
    } else {
      resetForm[field.key] = '';
    }
  });
  searchForm.value = resetForm;
  // 重置后自动触发搜索
  handleSearch();
};
</script>

<style scoped>
/* 使用 CSS Grid 实现响应式布局 - 社区最佳实践 */
.search-form-grid {
  display: grid;
  /* 使用 auto-fill 和 minmax 自动计算列数 */
  /* 普通字段最小宽度 200px，日期范围字段最小宽度 400px */
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem; /* 12px */
  align-items: end;
  width: 100%;
}

/* 普通字段样式 */
.search-form-item-normal {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0; /* 允许收缩 */
}

/* 日期范围字段 - 占据两列 */
.search-form-item-date-range {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  grid-column: span 2; /* 占据两列 */
  min-width: 0;
}

/* 按钮区域 - 自动适应 */
.search-form-actions {
  display: flex;
  align-items: end;
  grid-column: 1 / -1; /* 占据整行 */
  margin-top: 0.5rem;
}

/* 响应式断点优化 */
@media (min-width: 640px) {
  .search-form-grid {
    gap: 1rem; /* 16px */
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
  
  .search-form-item-date-range {
    grid-column: span 2;
    min-width: 400px;
  }
  
  .search-form-actions {
    grid-column: auto; /* 自动适应 */
    margin-top: 0;
  }
}

@media (min-width: 1024px) {
  .search-form-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
  
  .search-form-item-date-range {
    min-width: 450px;
  }
}

@media (min-width: 1280px) {
  .search-form-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
  
  .search-form-item-date-range {
    min-width: 500px;
  }
}

/* 日期范围容器 - 响应式布局 */
.date-range-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
  /* 不创建新的层叠上下文，允许子元素使用更高的 z-index */
  isolation: auto;
}

.date-picker-wrapper {
  flex: 1;
  min-width: 0;
  /* 不创建新的层叠上下文 */
  isolation: auto;
  position: relative;
}

.date-range-separator {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
  flex-shrink: 0;
  padding: 0 0.25rem;
}

/* 小屏幕优化 - 确保日期范围字段在小屏幕上也占据整行 */
@media (max-width: 639px) {
  .search-form-item-date-range {
    grid-column: 1 / -1; /* 占据整行 */
  }
  
  .date-range-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .date-picker-wrapper {
    width: 100%;
  }
  
  .date-range-separator {
    align-self: center;
    padding: 0.25rem 0;
  }
  
  .search-form-actions {
    grid-column: 1 / -1;
  }
  
  .search-form-actions .flex {
    width: 100%;
  }
  
  .search-form-actions .flex > button {
    flex: 1;
  }
}

/* 中等屏幕优化 */
@media (min-width: 640px) and (max-width: 1023px) {
  .date-range-container {
    gap: 0.5rem;
  }
  
  .date-picker-wrapper {
    min-width: 140px; /* 确保日期选择器有足够空间 */
  }
}

/* 大屏幕优化 */
@media (min-width: 1024px) {
  .date-range-container {
    gap: 0.75rem;
  }
  
  .date-picker-wrapper {
    min-width: 160px;
  }
}

/* 确保日期选择器弹窗在移动端显示在最上层 */
:deep([data-radix-popper-content-wrapper]) {
  z-index: 9999 !important;
}

:deep([data-radix-popper-content]) {
  z-index: 9999 !important;
}

@media (max-width: 639px) {
  :deep([data-radix-popper-content-wrapper]) {
    z-index: 10000 !important;
  }

  :deep([data-radix-popper-content]) {
    z-index: 10000 !important;
  }
}
</style>

