<template>
  <article class="overflow-x-hidden max-w-full whitespace-normal break-words [&_pre]:rounded [&_pre]:p-0 [&_pre]:overflow-x-auto [&_pre]:my-0 [&_code]:font-mono [&_code]:text-sm [&_p]:my-2 [&_ul]:pl-6 [&_ul]:my-2 [&_ol]:pl-6 [&_ol]:my-2 [&_table]:w-full [&_table]:my-2 [&_table]:border-collapse [&_th]:border [&_th]:border-gray-200 [&_th]:p-2 [&_th]:text-left [&_th]:bg-gray-50 [&_td]:border [&_td]:border-gray-200 [&_td]:p-2 [&_td]:text-left md:[&]:text-[13px] md:[&]:leading-[1.5]" ref="markdownRef">
    <div class="w-full overflow-x-auto [-webkit-overflow-scrolling:touch] box-border [&_table]:min-w-max [&_table]:w-auto [&_table]:max-w-none [&_table]:border-collapse [&_table]:box-border [&_table]:table [&_th]:whitespace-nowrap [&_th]:px-4 [&_th]:py-2 [&_td]:whitespace-nowrap [&_td]:px-4 [&_td]:py-2 md:[&]:max-w-full md:[&]:pb-2 md:[&_table]:text-xs md:[&_th]:text-xs md:[&_td]:text-xs">
      <template v-for="(block, index) in contentBlocks" :key="`block-${index}`">
        <!-- 代码块：使用 CodeMessage 组件 -->
        <CodeMessage
          v-if="block.type === 'code'"
          :code="block.code"
          :language="block.language"
        />
        <!-- 其他内容：使用 v-html -->
        <div v-else v-html="block.content" class="markdown-content-block"></div>
      </template>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, nextTick } from 'vue';
import { marked } from 'marked';
// @ts-ignore - DOMPurify 类型定义问题
import DOMPurify from 'dompurify';
import CodeMessage from './CodeMessage.vue';


interface Props {
  /** Markdown 内容 */
  content: string;
  /** 消息 ID（可选） */
  messageId?: string;
}

interface ContentRenderedEvent {
  type: 'markdown';
  messageId?: string;
  contentLength: number;
  isFirstRender: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  'content-rendered': [event: ContentRenderedEvent];
}>();

const markdownRef = ref<HTMLElement | null>(null);
const isFirstRender = ref(true);
const previousMessageId = ref<string | undefined>(undefined);

/**
 * 代码块信息接口
 */
interface CodeBlock {
  type: 'code';
  code: string;
  language?: string;
}

/**
 * 文本块信息接口
 */
interface TextBlock {
  type: 'text';
  content: string;
}

type ContentBlock = CodeBlock | TextBlock;

/**
 * 代码块正则表达式模式
 * 匹配格式：```language\ncode\n``` 或 ```language\ncode``` 
 * 允许语言标识符后有可选空格，支持 \r\n 和 \n 换行符
 */
const CODE_BLOCK_PATTERN = /```([a-zA-Z0-9_+-]*)\s*[\r\n]+([\s\S]*?)```/g;

/**
 * HTML 标签移除正则表达式
 * 匹配所有 HTML 标签（包括自闭合标签如 <br/>、<img/> 等）
 */
const HTML_TAG_PATTERN = /<[^>]+>/g;

/**
 * 处理文本内容：移除 HTML 标签并渲染为 Markdown
 */
const processTextContent = (text: string): string | null => {
  if (!text?.trim()) {
    return null;
  }
  
  // 移除所有 HTML 标签（包括自闭合标签）
  const textWithoutTags = text.replace(HTML_TAG_PATTERN, '').trim();
  if (!textWithoutTags) {
    return null;
  }
  
  // 渲染 Markdown 并清理
  const renderedText = marked.parse(textWithoutTags);
  return DOMPurify.sanitize(renderedText);
};

/**
 * 解析 Markdown 内容，提取代码块和文本块
 */
const parseMarkdownContent = (content: string): ContentBlock[] => {
  if (!content) {
    return [];
  }

  try {
    // 先提取代码块，然后再处理 HTML 标签
    // 这样可以避免 HTML 标签移除影响代码块匹配
    const blocks: ContentBlock[] = [];
    // 每次创建新的正则表达式实例，避免全局正则的 lastIndex 问题
    const codeBlockRegex = new RegExp(CODE_BLOCK_PATTERN.source, CODE_BLOCK_PATTERN.flags);
    let lastIndex = 0;
    let match: RegExpExecArray | null;
    const codeBlockPositions: Array<{ start: number; end: number; match: RegExpExecArray }> = [];

    // 第一步：在原始内容中找到所有代码块的位置
    while ((match = codeBlockRegex.exec(content)) !== null) {
      codeBlockPositions.push({
        start: match.index,
        end: codeBlockRegex.lastIndex,
        match: match
      });
    }
    
    // 第二步：按位置提取代码块和文本内容
    for (const codeBlockInfo of codeBlockPositions) {
      match = codeBlockInfo.match;
      
      // 添加代码块之前的文本内容
      const precedingText = content.substring(lastIndex, match.index);
      const processedText = processTextContent(precedingText);
      if (processedText) {
        blocks.push({
          type: 'text',
          content: processedText
        });
      }
      
      // 添加代码块（代码块内容不经过 HTML 标签移除）
      const language = match[1]?.trim() || undefined;
      const rawCode = match[2];
      const code = rawCode.replace(/^[\r\n]+|[\r\n]+$/g, '');
      
      blocks.push({
        type: 'code',
        code,
        language
      });

      lastIndex = codeBlockInfo.end;
    }

    // 添加剩余的文本内容
    const remainingText = content.substring(lastIndex);
    const processedRemainingText = processTextContent(remainingText);
    if (processedRemainingText) {
      blocks.push({
        type: 'text',
        content: processedRemainingText
      });
    }

    return blocks;
  } catch (error) {
    // 解析失败时返回原始内容作为文本块
    return [{
      type: 'text',
      content: DOMPurify.sanitize(content)
    }];
  }
};

// 配置 marked（模块级别，只执行一次）
marked.setOptions({
  breaks: true,
  gfm: true,
  pedantic: false,
  sanitize: false,
  smartLists: true,
  smartypants: true
} as any);

/**
 * 内容块列表
 */
const contentBlocks = computed<ContentBlock[]>(() => {
  return parseMarkdownContent(props.content);
});

/**
 * 检测内容是否是流式追加（新内容以旧内容开头）
 */
const isStreamingAppend = (newContent: string, oldContent: string): boolean => {
  if (!oldContent || !newContent) return false;
  // 新内容以旧内容开头，说明是流式追加
  return newContent.startsWith(oldContent);
};

/**
 * 监听 messageId 变化，重置首次渲染标志
 */
watch(() => props.messageId, (newMessageId) => {
  if (newMessageId !== previousMessageId.value) {
    isFirstRender.value = true;
    previousMessageId.value = newMessageId;
  }
}, { immediate: true });

/**
 * 监听内容变化，重置首次渲染标志
 */
watch(() => props.content, (newContent, oldContent) => {
  if (!newContent || newContent === oldContent) return;
  
  // 如果没有旧内容，肯定是首次渲染
  if (!oldContent) {
    isFirstRender.value = true;
    return;
  }
  
  // 如果是流式追加，不重置
  if (isStreamingAppend(newContent, oldContent)) {
    return;
  }
  
  // 其他情况（内容替换或大幅变化），重置首次渲染
  isFirstRender.value = true;
}, { immediate: false });

/**
 * 监听内容块变化，触发渲染完成事件
 */
watch(contentBlocks, () => {
  nextTick(() => {
    emit('content-rendered', {
      type: 'markdown',
      messageId: props.messageId,
      contentLength: props.content.length,
      isFirstRender: isFirstRender.value
    });
    
    // 设置为非首次渲染
    if (isFirstRender.value) {
      isFirstRender.value = false;
    }
  });
});

onMounted(() => {
  // 修正被 <p> 包裹的 table，保证横向滚动生效
  nextTick(() => {
    const wrapper = markdownRef.value;
    if (wrapper) {
      wrapper.querySelectorAll('p > table').forEach(table => {
        const p = table.parentElement;
        if (p && p.tagName === 'P') {
          p.replaceWith(table);
        }
      });
    }
  });
});
</script>

<style scoped>
/* 移动端适配 - 使用深度选择器覆盖 Markdown 渲染后的 HTML 元素样式（必须使用自定义样式，因为无法在模板中直接控制渲染后的 HTML） */
@media screen and (max-width: 768px) {
  /* 优化表格在移动端的显示 */
  :deep(table) {
    font-size: 11px !important;
  }
  
  :deep(th),
  :deep(td) {
    padding: 6px 8px !important;
    font-size: 11px !important;
  }
  
  /* 优化代码块在移动端的显示 */
  :deep(pre),
  :deep(code) {
    font-size: 11px !important;
    line-height: 1.4 !important;
    padding: 8px !important;
  }
  
  /* 优化段落和列表在移动端的显示 */
  :deep(p) {
    font-size: 13px !important;
    margin-top: 6px !important;
    margin-bottom: 6px !important;
  }
  
  :deep(ul),
  :deep(ol) {
    padding-left: 16px !important;
    margin-top: 6px !important;
    margin-bottom: 6px !important;
  }
  
  :deep(li) {
    font-size: 13px !important;
    margin-bottom: 4px !important;
  }
  
  /* 优化标题在移动端的显示 */
  :deep(h1) {
    font-size: 16px !important;
    margin-top: 10px !important;
    margin-bottom: 8px !important;
  }
  
  :deep(h2) {
    font-size: 15px !important;
    margin-top: 8px !important;
    margin-bottom: 6px !important;
  }
  
  :deep(h3) {
    font-size: 14px !important;
    margin-top: 8px !important;
    margin-bottom: 6px !important;
  }
  
  /* 优化内容块在移动端的显示 */
  .markdown-content-block {
    font-size: 13px !important;
    line-height: 1.5 !important;
  }
}
</style>
