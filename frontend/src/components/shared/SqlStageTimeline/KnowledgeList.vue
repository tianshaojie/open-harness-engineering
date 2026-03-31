<template>
  <div class="space-y-2 w-full max-w-full overflow-hidden">
    <div
      v-for="(item, idx) in items"
      :key="idx"
      class="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden transition-all w-full max-w-full min-w-0 box-border hover:border-gray-300 hover:shadow-sm"
    >
      <div class="flex items-center gap-2 p-3 bg-white cursor-pointer transition-all overflow-hidden w-full max-w-full min-w-0 box-border hover:bg-gray-50">
        <div class="flex items-start gap-2 flex-1 min-w-0">
          <span class="text-[11px] font-semibold text-gray-500 bg-gray-200 px-1.5 py-0.5 rounded flex-shrink-0">
            #{{ getItemIndex(item, idx) }}
          </span>
          <span
            class="text-[11px] font-semibold px-2 py-0.5 rounded uppercase flex-shrink-0"
            :class="getKnowledgeTypeClass(getItemType(item))"
          >
            {{ getItemType(item) }}
          </span>
          <h5
            class="flex-1 min-w-0 m-0 break-words text-[13px] font-medium text-gray-900"
            :title="getKnowledgeTitle(item)"
          >
            {{ getKnowledgeTitle(item) }}
          </h5>
        </div>
        <div class="flex items-center gap-2 flex-shrink-0 ml-2">
          <button
            type="button"
            class="text-xs text-blue-600 bg-transparent border-0 px-2 py-1 rounded cursor-pointer transition-all flex-shrink-0 hover:bg-blue-50 hover:text-blue-700"
            @click.stop="$emit('toggle-item', idx)"
          >
            {{ isExpanded(idx) ? '收起' : '展开' }}
          </button>
          <span
            v-if="getItemScore(item)"
            class="text-[11px] font-mono text-green-600 bg-green-50 px-1.5 py-0.5 rounded flex-shrink-0"
          >
            {{ Number(getItemScore(item)).toFixed(4) }}
          </span>
        </div>
      </div>

      <!-- 知识库项目内容 -->
      <KnowledgeItemContent
        v-if="isExpanded(idx)"
        :item="item"
        :get-knowledge-base-link="getKnowledgeBaseLink"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { SqlStageStateItem } from '@/views/chat/types';
import KnowledgeItemContent from './KnowledgeItemContent.vue';

interface KnowledgeItem {
  type?: string;
  index?: number;
  score?: number | string;
  question?: string;
  title?: string;
  name?: string;
  content_preview?: string;
  [key: string]: unknown;
}

interface Props {
  items: KnowledgeItem[];
  expandedItems: Record<string, boolean>;
  getKnowledgeBaseLink?: (item: KnowledgeItem) => string | undefined;
  getKnowledgeTitle: (item: KnowledgeItem) => string;
  getKnowledgeTypeClass: (type: string) => string;
  getItemKey: (idx: number) => string;
}

const props = defineProps<Props>();

defineEmits<{
  'toggle-item': [idx: number];
}>();

const getItemIndex = (item: KnowledgeItem, idx: number): number => {
  return (item.index as number) ?? idx + 1;
};

const getItemType = (item: KnowledgeItem): string => {
  return (item.type as string) || 'unknown';
};

const getItemScore = (item: KnowledgeItem): number | string | undefined => {
  return item.score;
};

const isExpanded = (idx: number): boolean => {
  return !!props.expandedItems[props.getItemKey(idx)];
};
</script>

