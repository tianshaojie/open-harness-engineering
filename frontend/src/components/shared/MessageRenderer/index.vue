<template>
  <div class="w-full contents">
    <!-- LoadingMessage 组件 -->
    <div 
      v-if="status === 'loading' && !content && !hasActiveReasoning" 
      class="flex items-center text-gray-600 text-sm md:text-xs"
    >
      <div class="flex items-center justify-center mr-2 animate-spin">
        <LoadingIcon class="w-4 h-4 md:w-3.5 md:h-3.5 text-indigo-500 animate-spin" />
      </div>
      <span>{{ loadingText }}</span>
    </div>
    <!-- ErrorMessage 组件 -->
    <div 
      v-else-if="status === 'failed'" 
      class="flex items-start text-[#d54941] text-sm md:text-xs px-3 py-2 md:px-2 md:py-1.5 bg-[rgba(213,73,65,0.1)] rounded mt-2 break-words min-w-0"
    >
      <ErrorIcon class="mr-2 mt-0.5 md:mt-[1.5px] text-[#d54941] flex-shrink-0 w-4 h-4" />
      <span class="flex-1 min-w-0 whitespace-pre-wrap leading-normal break-words">{{ content }}</span>
    </div>
    <template v-else>
      <!-- 根据内容类型显示不同组件 -->
      <template v-if="isAI && content">
        <template v-for="(block, i) in contentBlocks" :key="`${messageId}-${i}`">
          <CodeMessage v-if="block.type === 'code'" :code="block.value" :language="block.language" />
          <MarkdownMessage 
            v-else-if="block.type === 'markdown'" 
            :content="block.value"
            :messageId="messageId"
            @content-rendered="handleMarkdownContentRendered"
          />
          <p 
            v-else 
            class="whitespace-pre-wrap break-words leading-relaxed text-sm md:text-[13px] max-md:leading-[1.5]"
            v-html="formatTextContent(block.value)" 
          ></p>
        </template>
        <!-- data区：仅失败时显示 -->
        <div 
          v-if="dataMatch && dataMatch.isSuccess === false" 
          class="flex items-start text-[#d54941] text-sm md:text-xs px-3 py-2 md:px-2 md:py-1.5 bg-[rgba(213,73,65,0.1)] rounded mt-2 break-words min-w-0"
        >
          <ErrorIcon class="mr-2 mt-0.5 md:mt-[1.5px] text-[#d54941] flex-shrink-0 w-4 h-4" />
          <span class="flex-1 min-w-0 whitespace-pre-wrap leading-normal break-words">{{ dataMatch.msg }}</span>
        </div>
      </template>
      <!-- TextMessage 组件 -->
      <p 
        v-else-if="content" 
        class="whitespace-pre-wrap break-words leading-relaxed text-sm md:text-[13px] md:leading-normal max-md:leading-[1.5]" 
        v-html="formatTextContent(content)"
      ></p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, nextTick, ref } from 'vue';
import { useRoute } from 'vue-router';
import MarkdownMessage from './MarkdownMessage.vue';
import CodeMessage from './CodeMessage.vue';
import { LoadingIcon, ErrorIcon } from '@/assets/svg-icon';
import { useAgentChat } from '@/views/chat/chat-main/composables';
import type { ParsedMessage } from '@/views/chat/types';
import eventBus, { EventTypes } from '@/utils/eventBus';

/**
 * 组件常量配置
 */
const MESSAGE_CONFIG = {
  /** 最小内容长度阈值（用于判断是否需要解析） */
  MIN_CONTENT_LENGTH: 50,
  /** 文本内容更新最小长度阈值 */
  MIN_TEXT_UPDATE_LENGTH: 20,
  /** 默认代码语言 */
  DEFAULT_CODE_LANGUAGE: 'plaintext',
} as const;

/**
 * 内容块类型定义
 */
interface ContentBlock {
  type: 'code' | 'markdown' | 'text';
  value: string;
  language?: string;
}

/**
 * Data 匹配结果类型
 */
interface DataMatchResult {
  isSuccess: boolean;
  msg?: string;
  [key: string]: unknown;
}

interface Props {
  content: string;
  status: 'success' | 'loading' | 'failed';
  messageType: 'sender' | 'receiver';
  loadingText: string;
  hasActiveReasoning?: boolean;
  messageId?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  content: '',
  status: 'success',
  messageType: 'receiver',
  loadingText: '正在思考中...',
  hasActiveReasoning: false,
  messageId: undefined
});

// 组件名称定义
defineOptions({
  name: 'MessageRenderer'
});

// 使用 route 获取当前智能体ID（优化：使用 ref + watch 避免重复计算）
const route = useRoute();
const currentAgentId = ref<string>((route.params.agentId as string) || 'default');

watch(() => route.params.agentId, (newAgentId) => {
  currentAgentId.value = (newAgentId as string) || 'default';
}, { immediate: true });

// 使用 hook 获取解析方法
const agentChat = useAgentChat(currentAgentId.value);
const { parseMessage } = agentChat.parserActions;

// 判断是否为AI消息（用于决定是否渲染Markdown）
const isAI = computed(() => props.messageType === 'receiver');

// 解析消息内容（仅在 watch 中使用）
const getParsedMessage = (content: string): ParsedMessage => {
  if (!content || (props.status === 'loading' && content.length < MESSAGE_CONFIG.MIN_CONTENT_LENGTH)) {
    return { type: 'text', content };
  }
  return parseMessage(content);
};

/**
 * 将普通文本和 Markdown 混合的字符串解析为独立的块
 */
function parseTextAndMarkdown(text: string): ContentBlock[] {
  if (!text) return [];

  // 简单的 Markdown 检查
  const mdRegex = /(###|\*\*|`)/;
  if (mdRegex.test(text)) {
    return [{ type: 'markdown', value: text }];
  } else {
    return [{ type: 'text', value: text }];
  }
}

/**
 * 格式化文本内容（TextMessage 的功能）
 */
const formatTextContent = (content: string): string => {
  if (!content) return '';
  
  // 移除所有 HTML 标签及其内容
  const contentWithoutTags = content.replace(/<[^>]*>[\s\S]*?<\/[^>]*>/g, '');
  
  // 转义HTML特殊字符，避免XSS攻击
  const escaped = contentWithoutTags
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
  
  // 将换行符转换为<br>标签
  return escaped.replace(/\n/g, '<br>');
};

// 缓存正则表达式模式（优化性能：使用字符串模式，每次创建新实例避免 lastIndex 问题）
const QUESTION_TAG_PATTERN = '<question>[\\s\\S]*?</question>';
const QUESTION_TAG_PATTERN_FALLBACK = '<question>[\\s\\S]*';
const CODE_BLOCK_PATTERN = /```(\w*)\n([\s\S]*?)```/g;
const DATA_TAG_PATTERN = /<data>([\s\S]*?)<\/data>/;

/**
 * 解析内容块（优化：使用正则表达式模式，每次创建新实例避免状态污染）
 */
const contentBlocks = computed<ContentBlock[]>(() => {
  const content = (props.content || '')
    .replace(new RegExp(QUESTION_TAG_PATTERN, 'g'), '')
    .replace(new RegExp(QUESTION_TAG_PATTERN_FALLBACK), '');

  if (!content.trim()) {
    return [];
  }

  const blocks: ContentBlock[] = [];
  // 每次创建新的正则表达式实例，避免全局正则的 lastIndex 问题
  const codeBlockRegex = new RegExp(CODE_BLOCK_PATTERN.source, CODE_BLOCK_PATTERN.flags);
  let lastIndex = 0;
  let match;

  while ((match = codeBlockRegex.exec(content)) !== null) {
    const precedingText = content.substring(lastIndex, match.index);
    blocks.push(...parseTextAndMarkdown(precedingText));

    const language = match[1] || MESSAGE_CONFIG.DEFAULT_CODE_LANGUAGE;
    const code = match[2].trim();
    blocks.push({ type: 'code', language, value: code });

    lastIndex = codeBlockRegex.lastIndex;
  }

  const remainingText = content.substring(lastIndex);
  blocks.push(...parseTextAndMarkdown(remainingText));

  return blocks.filter(b => b.value.trim() !== '');
});

/**
 * 解析 data 标签内容（改进错误处理）
 */
const dataMatch = computed<DataMatchResult | null>(() => {
  const match = props.content.match(DATA_TAG_PATTERN);
  if (!match || !match[1]) {
    return null;
  }

  try {
    const parsed = JSON.parse(match[1]) as DataMatchResult;
    return parsed;
  } catch (error) {
    // 改进错误处理：记录错误但不影响渲染
    console.warn('[MessageRenderer] Failed to parse data tag:', error);
    return null;
  }
});

/**
 * 触发内容渲染完成事件
 */
const emitContentRendered = (type: 'text' | 'reasoning', contentLength: number, isFirstRender: boolean, forceScroll = false) => {
  nextTick(() => {
    eventBus.emit(EventTypes.CONTENT_RENDERED, {
      type,
      messageId: props.messageId,
      contentLength,
      isFirstRender,
      forceScroll
    });
  });
};

/**
 * 处理 MarkdownMessage 组件的内容渲染完成事件
 */
const handleMarkdownContentRendered = (event: { type: 'markdown'; messageId?: string; contentLength: number; isFirstRender: boolean }) => {
  nextTick(() => {
    eventBus.emit(EventTypes.CONTENT_RENDERED, {
      type: event.type,
      messageId: event.messageId || props.messageId,
      contentLength: event.contentLength,
      isFirstRender: event.isFirstRender
    });
  });
};

// 合并的 onMounted 生命周期钩子
onMounted(() => {
  // LoadingMessage 挂载时触发事件
  if (props.status === 'loading' && !props.content && !props.hasActiveReasoning) {
    emitContentRendered('reasoning', props.loadingText.length, true, true);
    return;
  }

  // 文本消息的渲染完成通知
  if (!contentBlocks.value.length && props.content) {
    emitContentRendered('text', props.content.length, true);
  }
});

// 监听内容变化（优化：添加更精确的条件判断）
watch(() => props.content, (newContent, oldContent) => {
  // 只有当内容真正发生变化且长度超过阈值时才触发
  if (!newContent || newContent === oldContent) {
    return;
  }

  const parsedMessage = getParsedMessage(newContent);
  if (parsedMessage.type === 'text' && newContent.length >= MESSAGE_CONFIG.MIN_TEXT_UPDATE_LENGTH) {
    emitContentRendered('text', newContent.length, false);
  }
});
</script>

<style scoped>
/* 仅保留必要的动画，其他样式使用 Tailwind */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 移动端适配 - 使用深度选择器覆盖子组件样式（必须使用自定义样式） */
@media screen and (max-width: 768px) {
  /* 优化代码块在移动端的显示 */
  :deep(pre),
  :deep(code) {
    font-size: 11px !important;
    line-height: 1.4 !important;
    padding: 8px !important;
  }
  
  /* 优化 Markdown 内容在移动端的显示 */
  :deep(.markdown-content) {
    font-size: 13px !important;
    line-height: 1.5 !important;
  }
  
  :deep(.markdown-content h1),
  :deep(.markdown-content h2),
  :deep(.markdown-content h3) {
    font-size: 14px !important;
    margin-top: 8px !important;
    margin-bottom: 6px !important;
  }
  
  :deep(.markdown-content p) {
    font-size: 13px !important;
    margin-bottom: 8px !important;
  }
  
  :deep(.markdown-content ul),
  :deep(.markdown-content ol) {
    font-size: 13px !important;
    padding-left: 16px !important;
  }
  
  :deep(.markdown-content li) {
    font-size: 13px !important;
    margin-bottom: 4px !important;
  }
}
</style>
