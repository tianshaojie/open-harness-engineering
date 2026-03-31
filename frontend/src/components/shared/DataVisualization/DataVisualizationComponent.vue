<template>
  <section :class="studioMode ? 'flex flex-col h-full' : 'flex flex-col mb-1.5'">
    <!-- 当只有数据错误信息且不在studio模式下时，直接显示错误，不显示任何标题 -->
    <div v-if="dataErrorMessage && !userData && !chartSuggestions && !chartErrorMessage && !studioMode">
      <DataDisplayComponent
        :userData="userData"
        :columns="columns"
        :dataErrorMessage="dataErrorMessage"
        :studioMode="studioMode"
        :maxHeight="maxHeight"
        :total-count="totalCount"
        :current-limit="currentLimit"
        :limit-source="limitSource"
        :is-refreshing="isRefreshing"
        @rendered="handleTableRendered"
        @table-rendered="handleTableRendered"
        @limit-change="emit('limitChange', $event)"
      />
    </div>

    <!-- 当有多个标签页时，显示完整的tabs组件 -->
    <Tabs v-else-if="hasMultipleTabs" v-model="activeTab" :class="studioMode ? 'w-full flex flex-col h-full' : 'w-full flex flex-col'">
      <div :class="studioMode ? 'flex flex-col h-full' : 'flex flex-col'">
      <!-- Tab行和执行时间显示 -->
      <div class="flex items-center justify-between mb-1.5">
        <TabsList>
          <TabsTrigger value="data">
            数据表格
          </TabsTrigger>
          <TabsTrigger
            value="charts"
            v-if="(chartSuggestions && chartSuggestions.length > 0) ||
                  chartErrorMessage ||
                  shouldShowChartTab"
          >
            图表展示
          </TabsTrigger>
          <TabsTrigger value="sql" v-if="!studioMode">
            SQL
          </TabsTrigger>
          <TabsTrigger value="create-api" v-if="studioMode">
            创建API
          </TabsTrigger>
        </TabsList>
        <!-- 执行时间显示插槽和导出按钮 - 只在数据表格TAB中显示 -->
        <div class="flex items-center gap-2" v-if="activeTab === 'data'">
          <slot name="execution-time" :executionTime="executionTime" :queryResult="queryResult">
            <!-- 默认不显示任何内容 -->
          </slot>
          <!-- 导出按钮插槽 - 根据 hideExportButton 控制显示 -->
          <slot v-if="!hideExportButton" name="export-actions" :userData="userData" :columns="columns">
            <!-- 默认不显示任何内容 -->
          </slot>
        </div>
      </div>

      <TabsContent value="data" :class="studioMode && activeTab === 'data' ? 'flex-1 min-h-0 flex flex-col' : studioMode ? 'hidden' : 'mb-2'">
        <DataDisplayComponent
          :userData="userData"
          :columns="columns"
          :dataErrorMessage="dataErrorMessage"
          :studioMode="studioMode"
          :maxHeight="maxHeight"
          :total-count="totalCount"
          :current-limit="currentLimit"
          :limit-source="limitSource"
          :is-refreshing="isRefreshing"
          @rendered="handleTableRendered"
          @table-rendered="handleTableRendered"
          @limit-change="emit('limitChange', $event)"
        />
      </TabsContent>

      <!-- 图表标签页，在以下情况显示：1)有图表数据 2)有图表错误信息 3)数据量符合图表显示条件 -->
      <TabsContent
        value="charts"
        :class="studioMode && activeTab === 'charts' ? '!mt-0 !mb-0 flex-1 min-h-0 flex flex-col bg-white' : studioMode ? 'hidden' : 'mb-2 bg-white'"
        v-if="(chartSuggestions && chartSuggestions.length > 0) ||
              chartErrorMessage ||
              shouldShowChartTab"
      >
        <ChartRecommendation
          :chartSuggestions="chartSuggestions"
          :chartErrorMessage="chartErrorMessage"
          :dataErrorMessage="dataErrorMessage"
          :loading="isChartLoading"
          :userData="userData"
          :columns="columns"
          :studioMode="studioMode"
          :maxHeight="maxHeight"
        />
      </TabsContent>

      <!-- SQL标签页（studio模式下不显示） -->
      <TabsContent 
        v-if="!studioMode"
        value="sql" 
        :class="sqlContainerClasses"
      >
        <div v-if="sql" class="flex flex-col">
          <CodeMessage
            :code="props.sql || ''"
            language="sql"
            :scrollable="true"
            class="h-full flex flex-col"
          />
        </div>
        <div v-else-if="activeTab === 'sql'" class="flex flex-col">
          <div class="h-full flex flex-col">
            <div class="flex items-center justify-center h-full">
              <EmptyState title="无有效SQL" />
            </div>
          </div>
        </div>
      </TabsContent>

      <!-- 创建API标签页内容 -->
      <!-- 只有切到 create-api TAB 时才强制挂载，避免在非激活 TAB 时触发 CreateApiForm 内的分组树请求 -->
      <TabsContent
        value="create-api"
        :class="studioMode && activeTab === 'create-api' ? 'flex-1 min-h-0 flex flex-col' : studioMode ? 'hidden' : 'mb-2'"
        v-if="studioMode"
        :force-mount="activeTab === 'create-api'"
      >
        <slot name="create-api-form">
          <!-- 默认的创建API表单插槽 -->
        </slot>
      </TabsContent>
      </div>
    </Tabs>

    <!-- 当只有一个标签页时，显示数据内容 -->
    <div v-else class="mb-2 flex flex-col">
      <!-- 当有数据或SQL执行成功时显示标题 -->
      <div v-if="(userData && userData.length > 0) || shouldShowDataTableTitle" class="mb-1.5 flex-shrink-0">
        <h3 class="text-sm font-medium text-gray-700">数据表格</h3>
      </div>

      <div>
        <!-- SQL语句显示 -->
        <div v-if="sql" class="mb-3 p-3 bg-gray-50 border border-gray-200 rounded-md">
          <div class="text-xs font-medium text-gray-600 mb-1.5">执行的SQL:</div>
          <pre class="text-xs text-gray-800 whitespace-pre-wrap font-mono">{{ sql }}</pre>
        </div>
        <DataDisplayComponent
          :userData="userData"
          :columns="columns"
          :dataErrorMessage="dataErrorMessage"
          :studioMode="studioMode"
          :maxHeight="maxHeight"
          :total-count="totalCount"
          :current-limit="currentLimit"
          :limit-source="limitSource"
          :is-refreshing="isRefreshing"
          @rendered="handleTableRendered"
          @table-rendered="handleTableRendered"
          @limit-change="emit('limitChange', $event)"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { DataDisplayComponent, ChartRecommendation } from './index';
import type { GenericData } from '@/views/chat/types';
import eventBus, { EventTypes } from '@/utils/eventBus';
import CodeMessage from '@/components/shared/MessageRenderer/CodeMessage.vue';
import EmptyState from '@/components/EmptyState/index.vue';

// Props定义，添加messageId属性用于区分不同消息
interface Props {
  userData: GenericData[] | null;
  columns: string[] | null;
  chartSuggestions: any[] | null;
  chartErrorMessage: string | null;
  dataErrorMessage: string | null;
  sql?: string | null; // SQL语句
  messageId?: string | number; // 添加消息ID，用于识别当前消息
  isStreamingMessage?: boolean; // 添加标识，用于区分历史消息和实时流式消息
  studioMode?: boolean; // 是否在studio模式下使用，限制表格高度
  maxHeight?: string; // 最大高度值，用于精确控制
  executionTime?: number; // 执行时间（毫秒）
  queryResult?: any; // 查询结果对象
  execRes?: number; // SQL执行结果，1表示成功，0表示失败
  defaultActiveTab?: 'data' | 'charts' | 'sql' | 'create-api'; // 默认激活的标签
  totalCount?: number; // 数据总数（通过COUNT查询获取）
  currentLimit?: number; // 当前的limit值
  limitSource?: string | null; // limit来源
  isRefreshing?: boolean; // 是否正在刷新SQL数据
  hideExportButton?: boolean; // 是否隐藏导出按钮（用于分享页面等场景）
}

const props = withDefaults(defineProps<Props>(), {
  userData: null,
  columns: null,
  chartSuggestions: null,
  chartErrorMessage: null,
  dataErrorMessage: null,
  sql: null,
  messageId: undefined,
  isStreamingMessage: false, // 默认为非流式消息
  studioMode: false, // 默认不使用studio模式
  maxHeight: '', // 默认无最大高度限制
  executionTime: undefined, // 默认无执行时间
  queryResult: undefined, // 默认无查询结果
  execRes: undefined, // 默认无执行结果
  defaultActiveTab: 'data',
  totalCount: undefined,
  currentLimit: undefined,
  limitSource: null,
  isRefreshing: false,
  hideExportButton: false
});

const emit = defineEmits<{
  (e: 'data-loaded'): void;
  (e: 'table-rendered'): void;
  (e: 'limitChange', limit: number): void;
}>();

// 从props直接获取数据，不再使用store
const userData = computed(() => props.userData);
const columns = computed(() => props.columns);

// 本地存储图表数据，从props获取
const chartSuggestions = ref<any[] | null>(props.chartSuggestions || null);
// 添加图表错误信息
const chartErrorMessage = ref<string | null>(props.chartErrorMessage || null);
// 添加数据错误信息
const dataErrorMessage = ref<string | null>(props.dataErrorMessage || null);

// 默认选中标签：优先使用传入的 defaultActiveTab
// 在studio模式下，如果默认是'sql'，则改为'data'（因为studio模式下不显示SQL tab）
const getInitialActiveTab = () => {
  const tab = props.defaultActiveTab || 'data';
  if (props.studioMode && tab === 'sql') {
    return 'data';
  }
  return tab;
};
const activeTab = ref(getInitialActiveTab());

// 当外部 defaultActiveTab 变化时，同步切换标签（支持路由后置激活）
watch(() => props.defaultActiveTab, (val) => {
  if (val && val !== activeTab.value) {
    // 在studio模式下，如果切换到'sql'，则改为'data'
    const targetTab = props.studioMode && val === 'sql' ? 'data' : val;
    activeTab.value = targetTab;
  }
});

// 当studioMode变化时，如果当前是'sql'标签，切换到'data'
watch(() => props.studioMode, (isStudioMode) => {
  if (isStudioMode && activeTab.value === 'sql') {
    activeTab.value = 'data';
  }
});

// 图表加载状态
const isChartLoading = ref(false);

// 计算数据量是否符合图表显示条件
const shouldShowChartTab = computed(() => {
  if (!userData.value || !Array.isArray(userData.value)) {
    return false;
  }
  
  const dataLength = userData.value.length;
  
  // 1条数据：不显示图表
  if (dataLength <= 1) {
    return false;
  }
  
  // 2条以上数据：显示图表
  return dataLength >= 2;
});

// 计算属性：判断是否有多个标签页
const hasMultipleTabs = computed(() => {
  // 在studio模式下，总是显示多个标签页（包含创建API标签页）
  if (props.studioMode) {
    return true;
  }
  // 如果有数据表格，就显示标签页（即使没有SQL也显示SQL标签页）
  const hasDataTable = (userData.value && userData.value.length > 0) || 
                       (columns.value && columns.value.length > 0) ||
                       props.execRes === 1 ||
                       !!props.dataErrorMessage;
  // 如果有图表或有数据表格，就显示标签页
  return shouldShowChartTab.value || hasDataTable;
});

// 计算是否应该显示数据表格标题
const shouldShowDataTableTitle = computed(() => {
  // 当SQL执行成功(execRes = 1)时，即使没有数据也显示标题
  return props.execRes === 1;
});

// 计算SQL容器样式（与数据表格容器保持一致）
const sqlContainerClasses = computed(() => {
  // 与数据表格的TabsContent保持一致，只有 mt-2 mb-2
  // 数据表格的TabsContent: studioMode && activeTab === 'data' ? 'flex-1 min-h-0 flex flex-col' : studioMode ? 'hidden' : 'mb-2'
  if (props.studioMode && activeTab.value === 'sql') {
    return 'flex-1 min-h-0 flex flex-col';
  } else if (props.studioMode) {
    return 'hidden';
  } else {
    return 'mb-2';
  }
});


// 计算属性：判断图表是否应该显示加载状态
const shouldShowLoading = computed(() => {
  // 在以下情况显示加载状态：
  // 1. 流式消息 + 有表格数据 + 数据量符合图表显示条件 + 无图表数据/错误
  return Boolean(
    props.isStreamingMessage && 
    userData.value && 
    userData.value.length > 0 && 
    shouldShowChartTab.value && // 只有数据量符合条件时才显示加载状态
    (!chartSuggestions.value || chartSuggestions.value.length === 0) && 
    !chartErrorMessage.value
  );
});

// 计算属性：判断是否有表格数据但没有图表数据
const hasTableDataButNoChartData = computed(() => {
  return userData.value && 
         userData.value.length > 0 && 
         (!chartSuggestions.value || chartSuggestions.value.length === 0) && 
         !chartErrorMessage.value &&
         shouldShowChartTab.value; // 只有数据量符合条件时才考虑显示图表
});

// 辅助函数：触发滚动到底部事件
const triggerScrollToBottom = () => {
  // 使用延时确保视图已更新
  setTimeout(() => {
    eventBus.emit(EventTypes.CONTENT_RENDERED, {
      type: 'visualization',
      messageId: props.messageId,
      contentLength: 1000,
      isFirstRender: true
    });
  }, 100);
};

// 监听原始数据和计算属性变化
watch(() => shouldShowLoading.value, (newValue) => {
  isChartLoading.value = newValue;
  
  // 添加超时保护，避免一直显示加载状态
  if (newValue) {
    setTimeout(() => {
      if (isChartLoading.value) {
        isChartLoading.value = false;
      }
    }, 30000); // 30秒超时
  }
});

// 当切换到图表标签且有原始数据但没有图表数据时，强制显示加载状态
watch(() => activeTab.value, (newValue) => {
  if (newValue === 'charts') {
    // 如果是流式消息且有表格数据但没有图表数据，显示加载状态
    if (props.isStreamingMessage && hasTableDataButNoChartData.value) {
      isChartLoading.value = true;
    } else if (shouldShowLoading.value) {
      isChartLoading.value = true;
    }
  }
  
  // 当切换标签页时触发滚动到底部
  triggerScrollToBottom();
}, { immediate: true });

// 监听用户数据变化，不再自动设置加载状态
watch(() => userData.value, (newValue) => {
  // 当用户数据发生变化时触发滚动到底部
  if (newValue && newValue.length > 0) {
    triggerScrollToBottom();
    
    // 保留加载状态设置，但移除自动切换标签页
    if (props.isStreamingMessage && hasTableDataButNoChartData.value) {
      isChartLoading.value = true;
    }
  }
}, { immediate: true, deep: true });

// 当props中的chartSuggestions变化时，更新本地数据
watch(() => props.chartSuggestions, (newValue) => {
  if (newValue) {
    chartSuggestions.value = newValue;
    // 图表数据已加载，关闭loading状态
    isChartLoading.value = false;
    
    if (newValue.length > 0) {
      // 移除自动切换到图表标签页的代码
      // 当图表数据加载完成时触发滚动到底部
      triggerScrollToBottom();
    }
  }
}, { immediate: true });

// 当props中的chartErrorMessage变化时，更新本地数据
watch(() => props.chartErrorMessage, (newValue) => {
  if (newValue) {
    chartErrorMessage.value = newValue;
    isChartLoading.value = false; // 有错误信息时停止加载状态
    // 即使有错误信息也触发滚动到底部
    triggerScrollToBottom();
  }
}, { immediate: true });

// 组件挂载时不再自动显示加载状态
onMounted(() => {
  // 组件挂载后触发滚动到底部
  triggerScrollToBottom();
});

// 监听数据表格相关数据变化，当表格数据加载完成时触发事件
watch(
  [
    () => props.userData,
    () => props.columns,
    () => props.dataErrorMessage
  ],
  () => {
    // 当有表格数据或表格错误信息时，触发表格渲染完成事件
    if (props.userData || props.dataErrorMessage) {
      nextTick(() => {
        emit('table-rendered');
      });
    }
  },
  { immediate: true }
);

// 监听图表相关数据变化，当图表数据加载完成时触发事件
watch(
  [
    () => props.chartSuggestions,
    () => props.chartErrorMessage
  ],
  () => {
    // 当有图表数据或图表错误信息时，触发数据加载完成事件
    if (props.chartSuggestions || props.chartErrorMessage) {
      nextTick(() => {
        emit('data-loaded');
      });
    }
  },
  { immediate: true }
);

// 处理表格渲染完成事件
const handleTableRendered = () => {
  nextTick(() => {
    emit('table-rendered');
  });
};

// 默认导出
defineExpose({});
</script> 
