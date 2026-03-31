<template>
  <div class="relative flex items-center">
    <PopoverRoot 
      :open="isOpen" 
      :on-open-change="handleOpenChange"
    >
      <PopoverTrigger as-child>
        <button 
          type="button" 
          class="calendar-trigger-button"
          @click="handleTriggerClick"
        >
          <div class="calendar-trigger">
            <Input
              :model-value="modelValue"
              :placeholder="placeholder"
              class="h-9 date-input"
              readonly
              @click.stop="handleTriggerClick"
            />
            <div 
              class="calendar-icon"
              @click.stop="handleTriggerClick"
            >
              <CalendarIcon class="calendar-icon-svg" />
            </div>
          </div>
        </button>
      </PopoverTrigger>
      <PopoverContent class="w-auto p-0 calendar-popover" :side="'bottom'" :align="'start'" :side-offset="4" :avoid-collisions="true">
        <div class="p-4 min-w-[280px] bg-white border border-gray-200 rounded-lg shadow-lg relative">
          <div class="flex items-center justify-between mb-4">
            <Button variant="ghost" size="sm" @click="previousMonth">
              <ChevronLeft class="h-4 w-4" />
            </Button>
            <span class="font-semibold text-sm">{{ calendarTitle }}</span>
            <Button variant="ghost" size="sm" @click="nextMonth">
              <ChevronRight class="h-4 w-4" />
            </Button>
          </div>
          <div class="flex flex-col gap-2">
            <div class="grid grid-cols-7 gap-1">
              <div v-for="day in weekDays" :key="day" class="text-center text-xs font-medium text-gray-500 p-1">{{ day }}</div>
            </div>
            <div class="grid grid-cols-7 gap-1">
              <div
                v-for="date in calendarDays"
                :key="date.key"
                :class="dateClass(date)"
                @click="selectDate(date)"
              >
                {{ date.day }}
              </div>
            </div>
          </div>
        </div>
      </PopoverContent>
    </PopoverRoot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ChevronLeft, ChevronRight } from 'lucide-vue-next';
import { PopoverRoot, PopoverTrigger, PopoverContent } from 'radix-vue';
import { CalendarIcon } from '@/assets/svg-icon';
import eventBus from '@/utils/eventBus';

const DATE_PICKER_OPEN = 'date-picker:open';
const DATE_PICKER_CLOSE = 'date-picker:close';
const instanceId = Symbol('date-picker-instance');

// 日历日期信息接口
interface CalendarDateInfo {
  key: number;
  day: number;
  date: Date;
  otherMonth: boolean;
  today: boolean;
  selected: boolean;
}

interface Props {
  modelValue?: string;
  placeholder?: string;
  selectedDate?: Date;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请选择日期',
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  'open': [];
}>();

// 星期几常量
const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

// 日历打开状态
const isOpen = ref(false);
const calendarMonth = ref(new Date());

// 日历标题
const calendarTitle = computed(() => {
  return `${calendarMonth.value.getFullYear()}年${calendarMonth.value.getMonth() + 1}月`;
});

// 生成日历天数
const generateCalendarDays = (month: Date, selectedDate?: Date): CalendarDateInfo[] => {
  const year = month.getFullYear();
  const monthIndex = month.getMonth();
  const firstDay = new Date(year, monthIndex, 1);
  const startDate = new Date(firstDay);
  startDate.setDate(startDate.getDate() - firstDay.getDay());
  
  const days: CalendarDateInfo[] = [];
  const today = new Date();
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    
    const isOtherMonth = date.getMonth() !== monthIndex;
    const isToday = date.toDateString() === today.toDateString();
    const isSelected = !!(selectedDate && date.toDateString() === selectedDate.toDateString());
    
    days.push({
      key: date.getTime(),
      day: date.getDate(),
      date: date,
      otherMonth: isOtherMonth,
      today: isToday,
      selected: isSelected
    });
  }
  
  return days;
};

// 日历天数
const calendarDays = computed(() => generateCalendarDays(calendarMonth.value, props.selectedDate));

// 日期样式类
const dateClass = (date: CalendarDateInfo): string => {
  const baseClass = 'aspect-square flex items-center justify-center text-sm cursor-pointer rounded transition-all';
  if (date.otherMonth) {
    return `${baseClass} text-gray-300 cursor-not-allowed`;
  }
  if (date.selected) {
    return `${baseClass} bg-gray-800 text-white font-semibold hover:bg-gray-700`;
  }
  if (date.today) {
    return `${baseClass} bg-blue-500 text-white font-semibold`;
  }
  return `${baseClass} hover:bg-gray-100`;
};

// 处理触发器点击
const handleTriggerClick = () => {
  if (!isOpen.value) {
    // 打开时，先关闭其他所有 DatePicker
    eventBus.emit(DATE_PICKER_CLOSE, instanceId);
    isOpen.value = true;
    emit('open');
    eventBus.emit(DATE_PICKER_OPEN, instanceId);
  } else {
    isOpen.value = false;
  }
};

// 处理弹窗状态变化（PopoverRoot 回调）
const handleOpenChange = (open: boolean) => {
  if (isOpen.value !== open) {
    isOpen.value = open;
    if (open) {
      emit('open');
    }
  }
};

// 处理点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  if (!isOpen.value) return;
  
  const target = event.target as HTMLElement;
  if (!target) return;
  
  const allPopoverContents = document.querySelectorAll('[data-radix-popper-content-wrapper]');
  const allTriggers = document.querySelectorAll('.calendar-trigger-button');
  
  const isClickInside = 
    Array.from(allPopoverContents).some(content => content.contains(target)) ||
    Array.from(allTriggers).some(trigger => trigger.contains(target));
  
  if (!isClickInside) {
    isOpen.value = false;
  }
};

// 处理其他 DatePicker 打开/关闭事件
const handleOtherDatePickerOpen = (openedInstanceId: unknown) => {
  if (openedInstanceId !== instanceId && isOpen.value) {
    isOpen.value = false;
  }
};

const handleDatePickerClose = (closedInstanceId: unknown) => {
  if (closedInstanceId !== instanceId && isOpen.value) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside, true);
  eventBus.on(DATE_PICKER_OPEN, handleOtherDatePickerOpen);
  eventBus.on(DATE_PICKER_CLOSE, handleDatePickerClose);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside, true);
  eventBus.off(DATE_PICKER_OPEN, handleOtherDatePickerOpen);
  eventBus.off(DATE_PICKER_CLOSE, handleDatePickerClose);
});

// 月份切换
const previousMonth = () => {
  calendarMonth.value = new Date(
    calendarMonth.value.getFullYear(),
    calendarMonth.value.getMonth() - 1,
    1
  );
};

const nextMonth = () => {
  calendarMonth.value = new Date(
    calendarMonth.value.getFullYear(),
    calendarMonth.value.getMonth() + 1,
    1
  );
};

// 日期格式化函数
const formatDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 选择日期
const selectDate = (dateInfo: CalendarDateInfo) => {
  if (!dateInfo.otherMonth) {
    emit('update:modelValue', formatDate(dateInfo.date));
    isOpen.value = false;
  }
};
</script>

<style scoped>
.calendar-trigger-button {
  @apply w-full relative;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.calendar-trigger {
  @apply relative flex items-center w-full;
  min-width: 0;
}

.calendar-trigger .date-input {
  @apply w-full min-w-0 cursor-pointer;
  /* 响应式最小宽度 */
  min-width: 120px;
}

.calendar-trigger .calendar-icon {
  @apply absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none select-none flex items-center justify-center;
}

.calendar-trigger .calendar-icon-svg {
  @apply w-4 h-4 shrink-0;
}

/* Popover 层级优化 - 确保日历弹窗显示在最上层 */
:deep([data-radix-popper-content-wrapper]) {
  z-index: 9999 !important;
}

:deep([data-radix-popper-content]) {
  z-index: 9999 !important;
}

.calendar-popover {
  z-index: 9999 !important;
}

/* 响应式优化 */
@media (max-width: 639px) {
  .calendar-trigger .date-input {
    min-width: 0;
    width: 100%;
  }
  
  /* 移动端更高的层级 */
  :deep([data-radix-popper-content-wrapper]) {
    z-index: 10000 !important;
  }

  :deep([data-radix-popper-content]) {
    z-index: 10000 !important;
  }

  .calendar-popover {
    z-index: 10000 !important;
  }
}

@media (min-width: 640px) and (max-width: 1023px) {
  .calendar-trigger .date-input {
    min-width: 140px;
  }
}

@media (min-width: 1024px) {
  .calendar-trigger .date-input {
    min-width: 160px;
  }
}
</style>

