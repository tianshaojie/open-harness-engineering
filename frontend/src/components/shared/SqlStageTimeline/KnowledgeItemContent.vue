<template>
  <div class="p-3 bg-gray-50 border-t border-gray-200">
    <div v-if="item.question || item.answer" class="space-y-2">
      <div v-if="item.question">
        <div class="text-xs font-semibold text-gray-700 mb-1">问题</div>
        <div class="text-xs text-gray-600 bg-white p-2 rounded">{{ item.question }}</div>
      </div>
      <div v-if="item.answer || item.content_preview">
        <div class="text-xs font-semibold text-gray-700 mb-1">回答</div>
        <div class="text-xs text-gray-600 bg-white p-2 rounded whitespace-pre-wrap max-h-64 overflow-y-auto">
          {{ item.answer || item.content_preview }}
        </div>
      </div>
    </div>

    <div v-else-if="item.type === 'table' || item.type === 'column'" class="space-y-2">
      <div v-if="item.name">
        <div class="text-xs font-semibold text-gray-700 mb-1">名称</div>
        <div class="text-xs text-blue-600 bg-white p-2 rounded font-mono">{{ item.name }}</div>
      </div>
      <div v-if="item.comment">
        <div class="text-xs font-semibold text-gray-700 mb-1">说明</div>
        <div class="text-xs text-gray-600 bg-white p-2 rounded">{{ item.comment }}</div>
      </div>
    </div>

    <div v-else-if="item.type === 'dsl'" class="space-y-2">
      <div v-if="item.name">
        <div class="text-xs font-semibold text-gray-700 mb-1">名称</div>
        <div class="text-xs text-green-600 bg-white p-2 rounded font-mono">{{ item.name }}</div>
      </div>
      <div v-if="item.content">
        <div class="text-xs font-semibold text-gray-700 mb-1">内容</div>
        <div class="text-xs text-gray-600 bg-white p-2 rounded [&_table]:text-xs [&_th]:text-xs [&_td]:text-xs">
          <MarkdownMessage :content="item.content" :messageId="`dsl-${item.data_id || item.file_id || ''}`" />
        </div>
      </div>
    </div>

    <div v-else-if="item.content || item.content_preview" class="space-y-2">
      <div class="text-xs font-semibold text-gray-700 mb-1">内容</div>
      <div class="text-xs text-gray-600 bg-white p-2 rounded whitespace-pre-wrap max-h-64 overflow-y-auto">
        {{ item.content || item.content_preview }}
      </div>
    </div>

    <div class="flex items-center gap-3 mt-3 pt-3 border-t border-gray-200 flex-wrap">
      <span v-if="item.file_id" class="text-xs text-gray-500">文件ID: {{ item.file_id }}</span>
      <span v-if="item.data_id" class="text-xs text-gray-500">数据ID: {{ item.data_id }}</span>
      <a
        v-if="knowledgeBaseLink"
        :href="knowledgeBaseLink"
        target="_blank"
        rel="noopener noreferrer"
        class="text-xs text-blue-600 no-underline px-2.5 py-1 rounded-md bg-blue-50 border border-blue-200 transition-all whitespace-nowrap ml-auto hover:text-blue-700 hover:bg-blue-100 hover:border-blue-300"
      >
        查看原文
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import MarkdownMessage from '@/components/shared/MessageRenderer/MarkdownMessage.vue';

interface Props {
  item: any;
  getKnowledgeBaseLink?: (item: any) => string | undefined;
}

const props = withDefaults(defineProps<Props>(), {
  getKnowledgeBaseLink: undefined,
});

const normalizeHost = (value: unknown): string | undefined => {
  if (typeof value !== 'string') return undefined;
  const trimmed = value.trim();
  if (!trimmed) return undefined;
  return trimmed.replace(/\/+$/, '');
};

const normalizeRuntimeEnv = (value: unknown): string => {
  const raw = typeof value === 'string' ? value.trim().toLowerCase() : '';
  if (!raw) return '';
  if (raw === 'development') return 'dev';
  if (raw === 'production') return 'prod';
  return raw;
};

const resolveCurrentEnv = (): string => {
  const envFromConfig = normalizeRuntimeEnv((import.meta as any).env?.VITE_APP_ENV);
  if (envFromConfig) {
    return envFromConfig;
  }
  return normalizeRuntimeEnv((import.meta as any).env?.MODE);
};

const resolveKnowledgeHost = (item: any): string => {
  const targetEnv = normalizeRuntimeEnv(item?.target_env);
  const currentEnv = resolveCurrentEnv();

  // 目标环境与当前环境一致时，始终走当前站点域名。
  if (targetEnv && currentEnv && targetEnv === currentEnv) {
    return window.location.origin;
  }

  if (targetEnv) {
    const envHostMap: Record<string, string | undefined> = {
      dev: (import.meta as any).env?.VITE_KNOWLEDGE_WEB_HOST_DEV,
      test: (import.meta as any).env?.VITE_KNOWLEDGE_WEB_HOST_TEST,
      prod: (import.meta as any).env?.VITE_KNOWLEDGE_WEB_HOST_PROD,
      unittest: (import.meta as any).env?.VITE_KNOWLEDGE_WEB_HOST_UNITTEST,
    };
    const mappedHost = normalizeHost(envHostMap[targetEnv]);
    if (mappedHost) {
      return mappedHost;
    }
  }

  return window.location.origin;
};

const knowledgeBaseLink = computed(() => {
  if (props.getKnowledgeBaseLink) {
    return props.getKnowledgeBaseLink(props.item);
  }
  // 如果没有传入函数，使用默认逻辑
  const { data_id, file_id, knowledge_code } = props.item;
  if (!data_id || !file_id || !knowledge_code) {
    return undefined;
  }
  const host = resolveKnowledgeHost(props.item);
  return `${host}/#/system/knowledge-base/${encodeURIComponent(knowledge_code)}/files/${encodeURIComponent(file_id)}?data_id=${encodeURIComponent(data_id)}`;
});
</script>
