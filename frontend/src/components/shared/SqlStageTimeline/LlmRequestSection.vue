<template>
  <div class="border border-gray-200 rounded-[10px] bg-white p-3">
    <div class="flex items-center justify-between gap-3 mb-2">
      <span class="text-[13px] font-semibold text-gray-900">{{ title }}</span>
      <div class="flex gap-2">
        <button
          type="button"
          class="text-xs text-green-600 bg-green-50 border border-green-200 rounded px-2.5 py-1 transition-all font-medium hover:bg-green-100 hover:border-green-300 hover:text-green-700"
          @click="handleCopy"
          :title="copyTitle"
        >
          复制
        </button>
        <button
          type="button"
          class="text-xs text-blue-600 bg-transparent border-0 cursor-pointer p-0 hover:underline"
          @click="toggle"
        >
          {{ isExpanded ? '收起' : '展开' }}
        </button>
      </div>
    </div>
    <div v-if="preview" class="text-xs text-gray-700 bg-gray-50 rounded-lg p-2 border border-dashed border-gray-200 break-words mb-2">
      {{ preview }}
    </div>
    <pre
      v-if="isExpanded"
      class="bg-slate-900 text-slate-100 rounded-lg text-xs font-mono p-2.5 whitespace-pre-wrap break-words overflow-wrap-break-word overflow-x-auto"
    >{{ formattedJson }}</pre>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

/**
 * LLM 请求/响应数据类型定义
 */
type LlmRequestData = {
  messages?: Array<Record<string, unknown>>;
  model?: string;
  app_code?: string;
  original_question?: string;
  [key: string]: unknown;
};

type LlmResponseData = {
  rewrite_success?: boolean;
  is_rewritten?: boolean;
  [key: string]: unknown;
};

type LlmData = LlmRequestData | LlmResponseData | Record<string, unknown>;

interface Props {
  title: string;
  data: LlmData;
  preview?: string;
  copyTitle?: string;
  expanded?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  preview: '',
  copyTitle: '复制',
  expanded: false,
});

const emit = defineEmits<{
  (e: 'toggle'): void;
  (e: 'copy', data: LlmData): void;
}>();

const isExpanded = computed(() => props.expanded);

const formattedJson = computed(() => {
  try {
    return JSON.stringify(props.data, null, 2);
  } catch (err) {
    return String(props.data);
  }
});

const toggle = () => {
  emit('toggle');
};

const handleCopy = () => {
  emit('copy', props.data);
};
</script>

