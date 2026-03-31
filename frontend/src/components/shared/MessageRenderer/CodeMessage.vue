<template>
  <article 
    class="bg-gray-50 rounded-xl border border-gray-200 shadow-sm"
    :class="[
      { 
        'my-2.5 max-md:my-2': !scrollable, 
        'flex flex-col flex-1 min-h-0 m-0': scrollable 
      },
      $attrs.class
    ]"
  >
    <header 
      class="flex justify-between items-center px-4 py-1.5 bg-gray-100 text-sm border-gray-200 max-md:text-[11px] max-md:px-2.5 max-md:py-1.5 rounded-t-xl"
      :class="{
        'flex-shrink-0': scrollable,
        'rounded-b-xl': isCollapsed,
        // 折叠时内容高度趋近 0，外层 article 底边框会与 header 底边框重叠
        // 这里去掉 header 的 border-b，清除重复线条
        'border-b border-gray-200': !isCollapsed,
        'border-b-0': isCollapsed
      }"
    >
      <span class="text-gray-600 font-medium font-sans flex items-center">{{ displayLanguage }}</span>
      <div class="flex items-center gap-3">
        <!-- 折叠/展开图标 -->
        <svg 
          width="24" 
          height="24" 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg" 
          class="text-gray-600 cursor-pointer p-1 max-md:w-5 max-md:h-5" 
          :class="{ 'rotate-180': !isCollapsed }"
          @click="toggleCollapse"
          :aria-label="isCollapsed ? '展开代码' : '收起代码'"
          :title="isCollapsed ? '展开代码' : '收起代码'"
        >
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        
        <!-- 复制图标 -->
        <svg 
          width="24" 
          height="24" 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg" 
          class="text-gray-600 cursor-pointer p-1 max-md:w-5 max-md:h-5"
          @click="copyCode"
          aria-label="Copy code"
          title="复制代码"
        >
          <path d="M8 4v12a2 2 0 002 2h8a2 2 0 002-2V8.342a2 2 0 00-.602-1.43l-4.364-4.364A2 2 0 0013.5 2H10a2 2 0 00-2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M16 18v2a2 2 0 01-2 2H6a2 2 0 01-2-2V9a2 2 0 012-2h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </header>
    <div
      class="transition-all duration-300 ease-in-out rounded-b-xl"
      :class="{
        'overflow-hidden': isCollapsed || !scrollable,
        'flex-1 min-h-0 overflow-y-auto overflow-x-hidden': scrollable && !isCollapsed
      }"
      :style="isCollapsed ? { maxHeight: '0px' } : (maxHeight && !scrollable ? { maxHeight } : {})"
    >
      <pre class="m-0 p-0 overflow-x-auto bg-transparent"><code ref="codeRef" :class="codeClass" class="font-mono text-sm leading-relaxed tab-size-2 p-4 block max-md:text-[11px] max-md:leading-[1.4] max-md:p-2"></code></pre>
    </div>
  </article>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick, onUnmounted } from 'vue';
import hljs from 'highlight.js/lib/core';
import sql from 'highlight.js/lib/languages/sql';
import 'highlight.js/styles/github.css';
import { toast } from '@/components/ui/toast/use-toast';
import { formatSqlWithFix } from '@/utils/sqlFormatter';

// 注册需要的语言
hljs.registerLanguage('sql', sql);

const props = defineProps({
  code: {
    type: String,
    required: true
  },
  language: {
    type: String,
    default: ''
  },
  maxHeight: {
    type: String,
    default: ''
  },
  scrollable: {
    type: Boolean,
    default: false
  },
});

const codeRef = ref(null);
const isCollapsed = ref(false);

const codeClass = computed(() => {
  return props.language ? `language-${props.language}` : '';
});

const displayLanguage = computed(() => {
  return props.language ? props.language.toUpperCase() : 'CODE';
});

// 检查是否为 SQL 代码
const isSqlCode = computed(() => {
  const lang = props.language?.toLowerCase() || '';
  return lang === 'sql' || lang === 'mysql' || lang === 'postgresql';
});

// 格式化后的代码
const formattedCode = computed(() => {
  if (!isSqlCode.value) {
    return props.code;
  }

  // formatSqlWithFix 内部已处理错误，直接调用即可
  return formatSqlWithFix(props.code, {
    tabWidth: 2,
    keywordCase: 'upper',
    linesBetweenQueries: 2,
  });
});

const highlightCode = () => {
  if (codeRef.value) {
    codeRef.value.textContent = formattedCode.value;
    hljs.highlightElement(codeRef.value);
  }
};

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

watch(() => props.code, () => {
  highlightCode();
});

onMounted(() => {
  highlightCode();
});

const copyCode = async () => {
  if (!formattedCode.value) return;
  
  // 检查 Clipboard API 是否可用
  if (!navigator.clipboard || !navigator.clipboard.writeText) {
    toast({title: '浏览器不支持剪贴板功能', variant: "error"});
    return;
  }
  
  try {
    await navigator.clipboard.writeText(formattedCode.value);
    toast({title: '代码已复制到剪贴板', variant: "success"});
  } catch (error) {
    console.error('复制到剪贴板失败:', error);
    const errorMsg = error instanceof Error ? error.message : '未知错误';
    toast({title: `复制失败: ${errorMsg}`, variant: "error"});
  }
};
</script>

<style scoped>
/* highlight.js 样式覆盖（必须使用自定义样式） */
.hljs {
  background: transparent;
}
</style>