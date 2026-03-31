<template>
  <div
    v-if="show"
    class="flex items-center justify-between py-2 px-0"
  >
    <div class="flex items-center gap-2 text-[13px] text-gray-900">
      <span class="font-semibold">智能数据查询</span>
      <span
        class="status-badge inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-xs font-medium"
        :class="statusBadgeClass"
      >
        <component
          :is="statusIcon"
          class="w-3 h-3"
          :class="{ 'animate-spin': status === 'processing' }"
        />
        {{ statusText }}
      </span>
      <span v-if="totalElapsedTime > 0" class="text-xs text-green-600 font-medium">
        总耗时 {{ formatElapsedTime(totalElapsedTime) }}
      </span>
      <span
        v-if="showTimeoutHint && totalElapsedTime >= 300 && timeoutHintVisible"
        class="text-xs text-amber-600 font-medium"
      >
        流程执行超过5分钟时会自动终止
      </span>
    </div>
    <div class="flex items-center gap-2">
      <div
        class="inline-flex items-center justify-center p-1.5 text-gray-500 hover:text-gray-700 rounded transition-all cursor-pointer"
        :aria-expanded="!collapsed"
        :aria-label="collapsed ? '展开步骤' : '收起流程'"
        @click="$emit('toggle')"
      >
        <component
          :is="collapseIcon"
          class="w-4 h-4 flex-shrink-0 transition-transform duration-200"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue';
import type { Component } from 'vue';
import type { SqlStageStatus } from '@/views/chat/types';
import { formatElapsedTime } from '@/views/chat/types';
import { ChevronUpIcon, ChevronRightIcon, SuccessIcon, FailedIcon, ProcessingIcon } from '@/assets/svg-icon';

const TIMEOUT_HINT_DURATION_MS = 5000;

interface Props {
  /** 是否显示头部 */
  show: boolean;
  /** 当前状态 */
  status: SqlStageStatus;
  /** 状态文本 */
  statusText: string;
  /** 总耗时（秒） */
  totalElapsedTime: number;
  /** 是否折叠 */
  collapsed: boolean;
  /** 是否显示单节点超时提示（历史消息不显示） */
  showTimeoutHint?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showTimeoutHint: true,
});

defineEmits<{
  toggle: [];
}>();

const timeoutHintVisible = ref(true);
let hintHideTimer: ReturnType<typeof setTimeout> | null = null;

watch(
  () => props.showTimeoutHint && props.totalElapsedTime >= 300,
  (shouldShow) => {
    if (hintHideTimer) {
      clearTimeout(hintHideTimer);
      hintHideTimer = null;
    }
    if (shouldShow) {
      timeoutHintVisible.value = true;
      hintHideTimer = setTimeout(() => {
        timeoutHintVisible.value = false;
        hintHideTimer = null;
      }, TIMEOUT_HINT_DURATION_MS);
    } else {
      timeoutHintVisible.value = false;
    }
  },
  { immediate: true }
);

onUnmounted(() => {
  if (hintHideTimer) {
    clearTimeout(hintHideTimer);
  }
});

const statusBadgeClass = computed(() => {
  const classMap: Record<SqlStageStatus, string> = {
    pending: 'bg-gray-100 text-gray-500 border border-gray-200',
    processing: 'bg-blue-50 text-blue-700 border border-blue-200 font-semibold animate-pulse',
    success: 'bg-green-100 text-green-800 border border-green-200 font-semibold',
    failed: 'bg-red-100 text-red-800 border border-red-200 font-semibold',
    skipped: 'bg-gray-50 text-gray-500 border border-gray-200',
  };
  return classMap[props.status] || 'bg-gray-100 text-gray-500 border border-gray-200';
});

const statusIcon = computed<Component>(() => {
  const iconMap: Record<SqlStageStatus, Component> = {
    success: SuccessIcon,
    failed: FailedIcon,
    processing: ProcessingIcon,
    pending: ProcessingIcon, // pending 状态也使用 processing 图标
    skipped: FailedIcon, // skipped 状态使用 failed 图标
  };
  return iconMap[props.status] || ProcessingIcon;
});

const collapseIcon = computed<Component>(() => {
  // 收起时显示右箭头（表示可展开），展开时显示上箭头（表示可收起）
  return props.collapsed ? ChevronRightIcon : ChevronUpIcon;
});
</script>

