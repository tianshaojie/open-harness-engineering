<template>
  <TooltipProvider>
    <div class="bg-white rounded-lg border border-gray-200 flex flex-col flex-1 min-h-0 overflow-hidden relative h-full z-[1]">
      <!-- 空数据/加载失败占位 -->
      <div v-if="displayData.length === 0" class="flex-1 flex flex-col justify-center items-center">
        <EmptyState
          :loading="isLoading"
          :title="emptyTitle"
          :description="emptyDescription"
        />
      </div>
      <!-- 表格内容 -->
      <div v-else class="flex-1 flex flex-col min-h-0 overflow-hidden">
          <!-- 隐藏测量容器：用于列宽自适应测量（避免操作 document.body） -->
          <div
            ref="measureContainerRef"
            class="fixed -left-[99999px] top-0 pointer-events-none opacity-0"
            aria-hidden="true"
          />
          <!-- PC端表格布局 - 表头和表体在同一滚动容器内 -->
          <div 
            ref="scrollContainerRef"
            :class="[
              'flex-1 overflow-y-auto overflow-x-auto min-h-0 z-[1] hidden md:block',
              isResizing ? 'select-none' : ''
            ]"
            @scroll="handleScroll"
            @wheel.passive="wheelHandler"
          >
            <Table 
              :class="tableClass" 
              class="min-w-full"
              overflow-x="auto"
            >
              <TableHeader class="sticky top-0 z-[5] bg-white border-b border-gray-200">
                <TableRow class="hover:bg-transparent border-none">
                  <TableHead
                    v-for="(col, colIndex) in columns"
                    :key="colIndex"
                    :ref="(el) => setHeaderRef(el, colIndex)"
                    :class="getHeaderCellClass(colIndex)"
                    :style="getColumnStyle(col, colIndex)"
                    @dblclick="copyColumnToClipboard(colIndex)"
                  >
                    <span class="pr-2">{{ col.title }}</span>
                    <!-- 竖向分割线（可拖拽调整该列宽度） -->
                    <div
                      v-if="colIndex !== columns.length - 1"
                      :class="getResizerClass(colIndex)"
                      @pointerdown.prevent="onResizePointerDown(colIndex, $event)"
                      @pointermove.prevent="onResizePointerMove"
                      @pointerup="onResizePointerUp"
                      @pointercancel="onResizePointerUp"
                      @lostpointercapture="onResizePointerUp"
                      @dblclick.stop.prevent="autoFitColumn(colIndex)"
                    >
                      <div class="resizer-line absolute top-0 left-1/2 -translate-x-1/2 h-full w-px bg-transparent"></div>
                    </div>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow 
                  v-for="(row, index) in displayData" 
                  :key="row.id" 
                  class="border-b border-gray-200 bg-white hover:bg-gray-50 transition-colors"
                >
                  <TableCell
                    v-for="(col, colIndex) in columns"
                    :key="colIndex"
                    :data-label="col.title"
                    :style="getColumnStyle(col, colIndex, true)"
                    class="table-cell-with-tooltip"
                  >
                    <!-- 插槽列 -->
                    <template v-if="col.slot">
                      <slot :name="col.slot" :row="row" :value="getCellValue(col, row)" :index="index" />
                    </template>
                    <!-- 操作列不显示tooltip -->
                    <template v-else-if="col.key === 'actions'">
                      <div :class="CELL_ELLIPSIS_CLASS">
                        <div v-if="col.render" :class="CELL_ELLIPSIS_CLASS" v-html="col.render!(getCellValue(col, row), row)"></div>
                        <span v-else :class="CELL_ELLIPSIS_CLASS">{{ renderCell(col, row) }}</span>
                      </div>
                    </template>
                    <!-- 普通列：使用 Tooltip 组件 -->
                    <template v-else>
                      <Tooltip 
                        :disabled="!shouldShowTooltip(col, row)"
                      >
                        <TooltipTrigger as-child>
                          <div 
                            :class="CELL_ELLIPSIS_CLASS"
                            class="cell-content"
                            @mouseenter="handleCellMouseEnter($event, col, row)"
                          >
                            <div v-if="col.render" :class="CELL_ELLIPSIS_CLASS" v-html="col.render!(getCellValue(col, row), row)"></div>
                            <span v-else :class="CELL_ELLIPSIS_CLASS">{{ renderCell(col, row) }}</span>
                          </div>
                        </TooltipTrigger>
                        <TooltipContent class="max-w-md whitespace-normal break-words">
                          <div v-html="getTooltipContent(col, row)" class="whitespace-normal break-words"></div>
                        </TooltipContent>
                      </Tooltip>
                    </template>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
      
        <!-- 移动端卡片布局 -->
        <div 
          ref="mobileScrollContainerRef"
          class="p-4 flex flex-col gap-4 overflow-y-auto md:hidden"
          @scroll="handleScroll"
          @wheel.passive="wheelHandler"
        >
          <div 
            v-for="row in displayData" 
            :key="row.id" 
            class="bg-white border border-gray-200 rounded-xl p-4 shadow-sm shrink-0 transition-all select-none touch-pan-y relative"
            :data-row-id="row.id"
          >
            <div 
              v-for="(col, colIndex) in columns" 
              :key="colIndex"
              class="flex items-start py-2 border-b border-gray-100 last:border-b-0 gap-2"
            >
              <div class="font-normal text-gray-700 mobile-col-title min-w-[80px] mr-2 shrink-0">{{ col.title }}</div>
              <div class="flex-1 text-gray-500 min-w-0 break-words mobile-col-content">
                <!-- 插槽列 -->
                <template v-if="col.slot">
                  <slot :name="col.slot" :row="row" :value="getCellValue(col, row)" :index="displayData.findIndex(r => r.id === row.id)" />
                </template>
                <!-- 操作列 -->
                <template v-else-if="col.key === 'actions'">
                  <div v-if="col.render" v-html="col.render!(getCellValue(col, row), row)"></div>
                  <span v-else>{{ renderCell(col, row) }}</span>
                </template>
                <!-- 普通列：支持 tooltip -->
                <template v-else>
                  <Tooltip 
                    :disabled="!shouldShowTooltip(col, row)"
                  >
                    <TooltipTrigger as-child>
                      <div 
                        class="cell-content-mobile break-words"
                        @mouseenter="handleCellMouseEnter($event, col, row)"
                      >
                        <div v-if="col.render" v-html="col.render!(getCellValue(col, row), row)"></div>
                        <span v-else>{{ renderCell(col, row) }}</span>
                      </div>
                    </TooltipTrigger>
                    <TooltipContent class="max-w-[90vw] whitespace-normal break-words">
                      <div v-html="getTooltipContent(col, row)" class="whitespace-normal break-words"></div>
                    </TooltipContent>
                  </Tooltip>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <Pagination
        v-if="showPagination"
        :total="displayTotal"
        :current-page="displayCurrentPage"
        :total-pages="totalPages"
        :page-size="isClientMode ? clientPageSize : props.pageSize"
        :page-size-options="props.pageSizeOptions"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      />
    </div>
  </TooltipProvider>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, reactive, onMounted, onUnmounted } from 'vue';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import EmptyState from '@/components/EmptyState/index.vue';
import Pagination from './Pagination.vue';
import { debounce } from '@/utils/functionUtils';
import { convertScientificNotation } from '@/utils/numberHelper';
import { toast } from '@/components/ui/toast/use-toast';

// 表格数据类型定义
export type TableData = Record<string, any> & {
  id: string | number;
};

// 表格列定义
export interface TableColumn {
  key: string;
  title: string;
  width?: string;
  render?: (value: any, row: TableData) => string;
  headerAlign?: 'left' | 'center' | 'right';
  align?: 'left' | 'center' | 'right';
  slot?: string;
}

interface Props {
  columns: TableColumn[];
  data: TableData[];
  loading?: boolean;
  /** 无数据或加载失败时的标题 */
  emptyTitle?: string;
  /** 无数据或加载失败时的描述 */
  emptyDescription?: string;
  showPagination?: boolean;
  paginationMode?: 'server' | 'client';
  total?: number;
  currentPage?: number;
  pageSize?: number;
  pageSizeOptions?: number[];
}

const props = withDefaults(defineProps<Props>(), {
  loading: undefined,
  emptyTitle: '暂无数据',
  emptyDescription: '',
  showPagination: true,
  paginationMode: 'server',
  total: 0,
  currentPage: 1,
  pageSize: () => 20,
  pageSizeOptions: () => [10, 20, 50, 100],
});

const emit = defineEmits<{
  'page-change': [page: number];
  'page-size-change': [size: number];
  'rendered': [];
}>();

// 是否需要显示横向滚动条（当表格总宽度超过容器时显示）
const needsHorizontalScroll = ref(false);

// 表格类名 - 始终使用固定布局
const tableClass = computed(() => {
  return 'table-fixed';
});

// 前端分页模式下的当前页
const clientCurrentPage = ref(1);
const clientPageSize = ref(props.pageSize);

// 客户端分页数据缓存
let cachedClientPage = 1;
let cachedClientPageSize = props.pageSize;
let cachedClientData: TableData[] | null = null;
let cachedDataRef: TableData[] | null = null;

// 是否为客户端分页模式
const isClientMode = computed(() => props.paginationMode === 'client');

// 前端分页数据
const clientPaginatedData = computed(() => {
  if (!isClientMode.value) return props.data;
  
  if (
    cachedClientPage === clientCurrentPage.value &&
    cachedClientPageSize === clientPageSize.value &&
    cachedDataRef === props.data &&
    cachedClientData
  ) {
    return cachedClientData;
  }
  
  const startIndex = (clientCurrentPage.value - 1) * clientPageSize.value;
  const endIndex = startIndex + clientPageSize.value;
  const result = props.data.slice(startIndex, endIndex);
  
  cachedClientPage = clientCurrentPage.value;
  cachedClientPageSize = clientPageSize.value;
  cachedDataRef = props.data;
  cachedClientData = result;
  
  return result;
});

// 实际显示的数据
const displayData = computed(() => {
  return isClientMode.value ? clientPaginatedData.value : props.data;
});

// 计算总页数
const totalPages = computed(() => {
  const total = isClientMode.value ? (props.data?.length || 0) : (props.total || 0);
  const pageSize = isClientMode.value ? clientPageSize.value : (props.pageSize || 20);
  return Math.max(1, Math.ceil(total / pageSize));
});

// 计算总数
const displayTotal = computed(() => {
  return isClientMode.value ? (props.data?.length || 0) : props.total;
});

// 计算当前页
const displayCurrentPage = computed(() => {
  return isClientMode.value ? clientCurrentPage.value : props.currentPage;
});


// 常量定义
const CELL_ELLIPSIS_CLASS = 'overflow-hidden text-ellipsis whitespace-nowrap max-w-full block';

// 表头宽度计算相关常量
const MIN_COLUMN_WIDTH = 150; // 最小列宽（px）
const MAX_COLUMN_WIDTH = 200; // 最大列宽（px）
const EXTRA_PADDING = 24; // 表头额外内边距（px）
const OVERFLOW_THRESHOLD = 1; // 溢出判断阈值（px）
// 分配列宽时预留的宽度：纵向滚动条 + 舍入误差，避免 100% 时撑出横向滚动条
const CONTAINER_WIDTH_RESERVE = 20;

// 列宽类型定义
type ColumnWidthType = 'px' | 'percent' | 'auto';

interface ParsedWidth {
  type: ColumnWidthType;
  value: number; // 像素值或百分比值（0-100）
}

// 防抖延迟时间（ms）
const DEBOUNCE_DELAY = 150; // Tooltip 溢出检测防抖
const HEADER_WIDTH_DEBOUNCE_DELAY = 200; // 表头宽度计算防抖

// 移动端列标题最小宽度（px）
const MOBILE_COL_TITLE_MIN_WIDTH = 80;

// 内部 loading 状态（根据数据变化自动判断，或使用外部传入的 loading）
const internalLoading = ref(false);

// 计算最终的 loading 状态：优先使用外部传入的 loading，否则使用内部判断的 loading
const isLoading = computed(() => {
  if (props.loading !== undefined) {
    return props.loading;
  }
  return internalLoading.value;
});

// 溢出状态映射，key: `${colKey}-${rowId}`，使用对象以确保响应式更新
const overflowMap = reactive<Record<string, boolean>>({});
// 溢出检测缓存，避免重复计算
const overflowCache = new Map<string, boolean>();
// 溢出检测防抖定时器映射（每个单元格独立防抖）
const overflowDebounceTimers = new Map<string, number>();

// 清理溢出缓存（数据变化时调用）
const clearOverflowCache = () => {
  overflowCache.clear();
  // 清理所有防抖定时器
  overflowDebounceTimers.forEach(timer => {
    if (timer) {
      window.clearTimeout(timer);
    }
  });
  overflowDebounceTimers.clear();
  Object.keys(overflowMap).forEach(key => {
    delete overflowMap[key];
  });
};

// 实际的溢出检测逻辑
const checkOverflow = (element: HTMLElement, col: TableColumn, row: TableData) => {
  const key = `${col.key}-${row.id}`;
  const value = getCellValue(col, row);
  
  // 如果值为空，不显示 tooltip
  if (isEmptyValue(value)) {
    overflowMap[key] = false;
    overflowDebounceTimers.delete(key);
    return;
  }
  
  // 检查缓存
  if (overflowCache.has(key)) {
    overflowMap[key] = overflowCache.get(key)!;
    overflowDebounceTimers.delete(key);
    return;
  }
  
  // 使用 requestAnimationFrame 确保在下一帧测量，此时布局已完成
  requestAnimationFrame(() => {
    // 直接测量外层容器（cell-content div）
    const contentElement = element;
    
    // 确保元素可见且有尺寸
    if (!contentElement || contentElement.offsetWidth === 0) {
      overflowMap[key] = false;
      overflowCache.set(key, false);
      overflowDebounceTimers.delete(key);
      return;
    }
    
    const clientWidth = contentElement.clientWidth;
    let scrollWidth = contentElement.scrollWidth;
    
    // 如果 scrollWidth 为 0，尝试测量内部元素的宽度
    if (scrollWidth === 0 || scrollWidth === clientWidth) {
      const firstChild = contentElement.firstElementChild as HTMLElement;
      if (firstChild) {
        // 创建一个临时测量元素来获取真实宽度
        const measureEl = firstChild.cloneNode(true) as HTMLElement;
        const computedStyle = window.getComputedStyle(firstChild);
        
        // 设置测量元素的样式
        measureEl.style.position = 'absolute';
        measureEl.style.visibility = 'hidden';
        measureEl.style.width = 'auto';
        measureEl.style.maxWidth = 'none';
        measureEl.style.overflow = 'visible';
        measureEl.style.whiteSpace = computedStyle.whiteSpace || 'nowrap';
        measureEl.style.display = 'inline-block';
        measureEl.style.fontSize = computedStyle.fontSize;
        measureEl.style.fontFamily = computedStyle.fontFamily;
        measureEl.style.fontWeight = computedStyle.fontWeight;
        measureEl.style.letterSpacing = computedStyle.letterSpacing;
        
        document.body.appendChild(measureEl);
        scrollWidth = Math.max(scrollWidth, measureEl.offsetWidth);
        document.body.removeChild(measureEl);
      }
    }
    
    const isOverflowing = scrollWidth > clientWidth + OVERFLOW_THRESHOLD;
    
    // 更新缓存和响应式状态
    overflowCache.set(key, isOverflowing);
    overflowMap[key] = isOverflowing;
    overflowDebounceTimers.delete(key);
  });
};

// 处理单元格鼠标进入事件，实时检测溢出（带防抖和缓存）
const handleCellMouseEnter = (event: MouseEvent, col: TableColumn, row: TableData) => {
  const element = event.currentTarget as HTMLElement;
  if (!element) {
    return;
  }
  
  const key = `${col.key}-${row.id}`;
  
  // 如果已有定时器，清除它
  const existingTimer = overflowDebounceTimers.get(key);
  if (existingTimer) {
    window.clearTimeout(existingTimer);
  }
  
  // 设置新的防抖定时器
  const timer = window.setTimeout(() => {
    checkOverflow(element, col, row);
  }, DEBOUNCE_DELAY);
  
  overflowDebounceTimers.set(key, timer);
};

// 滚动容器引用
const scrollContainerRef = ref<HTMLElement | null>(null);
const measureContainerRef = ref<HTMLElement | null>(null);
const mobileScrollContainerRef = ref<HTMLElement | null>(null);
// ResizeObserver 引用，用于监听容器大小变化
const resizeObserverRef = ref<ResizeObserver | null>(null);
// 表头引用映射
const headerRefs = reactive<Record<number, HTMLElement | null>>({});
// 列宽映射，使用索引作为key以支持重复列名
const columnWidths = reactive<Record<number, number>>({});
// 用户拖拽后的列宽（px），优先级高于 columns.width 配置与自动计算
const userResizedWidths = reactive<Record<number, number>>({});
// 解析后的列宽配置，使用索引作为key
const parsedColumnWidths = reactive<Record<number, ParsedWidth | null>>({});
// 容器宽度，用于计算百分比列宽
const containerWidth = ref(0);

// 列分割线拖拽相关
const RESIZE_MIN_COLUMN_WIDTH = 80; // 拖拽时允许的最小列宽（px）
const isResizing = ref(false);
const activeResizeColIndex = ref<number | null>(null);
const resizeState = ref<{
  colIndex: number;
  startX: number;
  startWidth: number;
} | null>(null);
const resizeRafId = ref<number | null>(null);
const lastResizeClientX = ref<number | null>(null);
const needsOverflowRecheckAfterResize = ref(false);
const hasGlobalResizeEndListeners = ref(false);

const isActiveResizeColumn = (colIndex: number) => activeResizeColIndex.value === colIndex;

const getHeaderCellClass = (colIndex: number) => {
  // 表头竖向分割线默认不显示（border 透明），hover 表头区域时才显示
  const base = 'px-3 py-3 font-semibold text-gray-700 align-middle bg-white whitespace-nowrap relative border-r border-transparent last:border-r-0';
  return isActiveResizeColumn(colIndex) ? `${base} col-resizing` : base;
};

const getResizerClass = (colIndex: number) => {
  const base = 'column-resizer absolute top-0 right-0 h-full w-3 translate-x-1/2 cursor-col-resize select-none touch-none z-10';
  return isActiveResizeColumn(colIndex) ? `${base} is-active` : base;
};

const AUTO_FIT_EXTRA_WIDTH = 24; // 为 padding/余量预留的额外宽度（px）
const AUTO_FIT_MAX_WIDTH = 2000; // 防止极端内容导致无限增宽

const measureIntrinsicWidth = (el: HTMLElement): number => {
  const computedStyle = window.getComputedStyle(el);
  const measureEl = el.cloneNode(true) as HTMLElement;

  measureEl.style.position = 'absolute';
  measureEl.style.visibility = 'hidden';
  measureEl.style.width = 'auto';
  measureEl.style.maxWidth = 'none';
  measureEl.style.overflow = 'visible';
  measureEl.style.whiteSpace = computedStyle.whiteSpace || 'nowrap';
  measureEl.style.display = 'inline-block';
  measureEl.style.fontSize = computedStyle.fontSize;
  measureEl.style.fontFamily = computedStyle.fontFamily;
  measureEl.style.fontWeight = computedStyle.fontWeight;
  measureEl.style.letterSpacing = computedStyle.letterSpacing;

  const container = measureContainerRef.value || document.body;
  container.appendChild(measureEl);
  const width = measureEl.offsetWidth || 0;
  container.removeChild(measureEl);
  return width;
};

const getColumnContentWidth = (td: HTMLElement): number => {
  // 优先测量我们用于展示内容的容器
  const contentEl = td.querySelector<HTMLElement>('.cell-content');
  if (contentEl) {
    // 如果已经不溢出，scrollWidth 会等于 clientWidth，需测真实内容宽度避免“每次双击+余量继续增宽”
    const sw = contentEl.scrollWidth || 0;
    const cw = contentEl.clientWidth || 0;
    if (sw > cw + 1) return sw;

    const inner = contentEl.firstElementChild as HTMLElement | null;
    return inner ? measureIntrinsicWidth(inner) : measureIntrinsicWidth(contentEl);
  }

  // 操作列 / 非标准内容兜底
  return td.scrollWidth || td.offsetWidth || 0;
};

const htmlToPlainText = (html: string): string => {
  const container = measureContainerRef.value || document.body;
  const div = document.createElement('div');
  div.innerHTML = html;
  container.appendChild(div);
  const text = (div.textContent || '').trim();
  container.removeChild(div);
  return text;
};

const getCopyValue = (col: TableColumn, row: TableData): string => {
  // 操作列不复制
  if (col.key === 'actions') return '';

  const value = getCellValue(col, row);
  if (isEmptyValue(value)) return '';

  // 插槽列：无法拿到渲染后的内容，使用原始值
  if (col.slot) {
    if (typeof value === 'string') return value.replace(/\s+/g, ' ').trim();
    if (typeof value === 'number' || typeof value === 'boolean') return String(value);
    try {
      return JSON.stringify(value);
    } catch {
      return String(value);
    }
  }

  // render 可能返回 HTML
  if (col.render) {
    const html = col.render(value, row);
    const text = htmlToPlainText(html);
    return text.replace(/\s+/g, ' ').trim();
  }

  // 普通列：沿用现有科学计数法处理
  return convertScientificNotation(value).replace(/\s+/g, ' ').trim();
};

const writeClipboardText = async (text: string) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  throw new Error('Clipboard API not available');
};

const getDomColumnValues = (colIndex: number): string[] | null => {
  if (!scrollContainerRef.value) return null;
  const rows = Array.from(scrollContainerRef.value.querySelectorAll('tbody tr'));
  if (rows.length === 0) return [];

  return rows.map((row) => {
    const td = row.children.item(colIndex) as HTMLElement | null;
    if (!td) return '';
    const text = (td.innerText || td.textContent || '').replace(/\s+/g, ' ').trim();
    return text;
  });
};

const copyColumnToClipboard = async (colIndex: number) => {
  const col = props.columns[colIndex];
  if (!col || col.key === 'actions') return;

  // 优先从 DOM 拿到“用户实际看到的文本”（兼容 slot / render / v-html）
  const domValues = getDomColumnValues(colIndex);
  const values = (domValues ?? displayData.value.map((row) => getCopyValue(col, row))).map((v) => v ?? '');
  const text = values.join(',');

  try {
    await writeClipboardText(text);
    toast({ title: '复制成功', variant: 'success' });
  } catch {
    toast({ title: '复制失败', variant: 'error' });
  }
};

const autoFitColumn = (colIndex: number) => {
  if (!scrollContainerRef.value) return;
  if (isResizing.value) onResizePointerUp();

  const headerEl = headerRefs[colIndex];
  const headerTextEl = headerEl?.querySelector<HTMLElement>('span');
  const headerWidth = headerTextEl
    ? (() => {
        const sw = headerTextEl.scrollWidth || 0;
        const cw = headerTextEl.clientWidth || 0;
        return sw > cw + 1 ? sw : measureIntrinsicWidth(headerTextEl);
      })()
    : (headerEl ? (headerEl.scrollWidth || headerEl.offsetWidth || 0) : 0);

  // 只按当前页可见数据计算（性能/体验折中）
  const rows = Array.from(scrollContainerRef.value.querySelectorAll('tbody tr'));
  let maxWidth = headerWidth;

  for (const row of rows) {
    const td = row.children.item(colIndex) as HTMLElement | null;
    if (!td) continue;
    maxWidth = Math.max(maxWidth, getColumnContentWidth(td));
  }

  const nextWidth = Math.min(
    AUTO_FIT_MAX_WIDTH,
    Math.max(RESIZE_MIN_COLUMN_WIDTH, Math.ceil(maxWidth + AUTO_FIT_EXTRA_WIDTH))
  );

  const currentWidth = getCurrentColumnWidth(colIndex);
  const finalWidth = nextWidth > currentWidth ? nextWidth : currentWidth;

  userResizedWidths[colIndex] = finalWidth;
  columnWidths[colIndex] = finalWidth;
  updateHorizontalScrollFlag();
  clearOverflowCache();
};

// 处理滚动事件（Tooltip 会自动处理关闭，这里保留用于其他可能的清理）
const handleScroll = () => {
  // Radix Vue Tooltip 会自动处理滚动时关闭，这里不需要手动处理
};

// 滚动事件处理器（用于触摸板）
const wheelHandler = () => {
  handleScroll();
};

// 检查是否应该显示 tooltip
// 只有在内容溢出时才显示 tooltip
const shouldShowTooltip = (col: TableColumn, row: TableData): boolean => {
  const value = getCellValue(col, row);
  if (isEmptyValue(value)) {
    return false;
  }
  
  const key = `${col.key}-${row.id}`;
  // 检查 overflowMap 中是否有溢出标记
  return overflowMap[key] === true;
};

// 检查值是否为空
const isEmptyValue = (value: any): boolean => {
  return value === null || value === undefined || value === '' || (typeof value === 'string' && value.trim() === '');
};

// 清理客户端分页缓存
const clearClientPaginationCache = (newPageSize?: number) => {
  clientCurrentPage.value = 1;
  cachedClientPage = 1;
  cachedClientData = null;
  cachedDataRef = null;
  if (newPageSize !== undefined) {
    cachedClientPageSize = newPageSize;
  }
};

// 合并的 watch：监听数据变化，处理 loading 状态和数据更新
watch(
  () => props.data,
  (newData, oldData) => {
    const newLength = newData?.length || 0;
    const oldLength = oldData?.length || 0;
    
    // 处理内部 loading 状态（仅在外部未传入 loading 时使用）
    if (props.loading === undefined) {
      if (oldLength > 0 && newLength === 0) {
        internalLoading.value = true;
      } else if (newLength > 0) {
        internalLoading.value = false;
      } else if (oldLength > 0 && newLength > 0 && newData !== oldData) {
        internalLoading.value = true;
        setTimeout(() => {
          internalLoading.value = false;
        }, 100);
      }
    }
    
    // 处理数据变化（如果不是同一个引用）
    if (newData !== oldData) {
      nextTick(() => {
        if (isClientMode.value) {
          clearClientPaginationCache();
        }
        
        // 清理溢出缓存
        clearOverflowCache();
        
        // 重新计算表头宽度
        calculateHeaderWidths();
        
        emit('rendered');
      });
    }
  },
  { immediate: true }
);

// 监听列定义变化，重新计算表头宽度（优化：只监听列数量变化，而不是深度监听）
watch(
  () => props.columns.length,
  () => {
    nextTick(() => {
      Object.keys(userResizedWidths).forEach((key) => {
        delete userResizedWidths[parseInt(key, 10)];
      });
      calculateHeaderWidths();
    });
  }
);

// 单独监听列 key 变化（列顺序或列替换）
watch(
  () => props.columns.map(col => col.key).join(','),
  () => {
    nextTick(() => {
      Object.keys(userResizedWidths).forEach((key) => {
        delete userResizedWidths[parseInt(key, 10)];
      });
      calculateHeaderWidths();
    });
  }
);

// 监听列宽度配置变化
watch(
  () => props.columns.map(col => col.width || '').join(','),
  () => {
    // 清空已解析的列宽配置和计算出的列宽，强制重新计算
    Object.keys(parsedColumnWidths).forEach(key => {
      delete parsedColumnWidths[parseInt(key)];
    });
    Object.keys(columnWidths).forEach(key => {
      delete columnWidths[parseInt(key)];
    });
    Object.keys(userResizedWidths).forEach((key) => {
      delete userResizedWidths[parseInt(key, 10)];
    });
    // 立即触发重新计算，不使用防抖
    nextTick(() => {
      // 先解析所有列的宽度配置
      props.columns.forEach((col, index) => {
        parsedColumnWidths[index] = parseColumnWidth(col.width);
      });
      // 直接调用计算函数，不使用防抖
      if (scrollContainerRef.value) {
        const currentContainerWidth = scrollContainerRef.value.clientWidth;
        if (currentContainerWidth > 0) {
          // 直接计算，不使用防抖
          calculateColumnWidths();
        } else {
          // 如果容器宽度为0，延迟执行
          setTimeout(() => {
            calculateHeaderWidths();
          }, 100);
        }
      } else {
        calculateHeaderWidths();
      }
    });
  }
);

// 分页切换
const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  if (isClientMode.value) {
    clientCurrentPage.value = page;
  } else {
    emit('page-change', page);
  }
};

// 每页条数变化
const handlePageSizeChange = (value: string | number) => {
  const newSize = typeof value === 'string' ? parseInt(value, 10) : value;
  if (isClientMode.value) {
    clientPageSize.value = newSize;
    clearClientPaginationCache(newSize);
  } else {
    emit('page-size-change', newSize);
  }
};

// 设置表头引用
const setHeaderRef = (el: any, colIndex: number) => {
  if (el) {
    // 如果是 Vue 组件实例，获取其 DOM 元素
    let domEl: HTMLElement | null = null;
    if (el.nodeType === 1) {
      // 已经是 DOM 元素
      domEl = el as HTMLElement;
    } else if (el.$el) {
      // Vue 组件实例
      domEl = el.$el as HTMLElement;
    } else if (typeof el === 'object' && 'style' in el) {
      // 可能是包装后的元素
      domEl = el as HTMLElement;
    }
    
    if (domEl && domEl.nodeType === 1) {
      headerRefs[colIndex] = domEl;
    }
  }
};

// 解析列宽配置
const parseColumnWidth = (width: string | undefined): ParsedWidth | null => {
  if (!width) return null;
  
  const trimmed = width.trim();
  
  // 解析像素值（如 "150px", "200px"）
  const pxMatch = trimmed.match(/^(\d+(?:\.\d+)?)px$/i);
  if (pxMatch) {
    const value = parseFloat(pxMatch[1]);
    if (value > 0 && isFinite(value)) {
      return { type: 'px', value };
    }
  }
  
  // 解析百分比值（如 "20%", "30%"）
  const percentMatch = trimmed.match(/^(\d+(?:\.\d+)?)%$/);
  if (percentMatch) {
    const value = parseFloat(percentMatch[1]);
    if (value >= 0 && value <= 100 && isFinite(value)) {
      return { type: 'percent', value };
    }
  }
  
  // 其他情况返回 null，使用自动计算
  return null;
};

// 计算列宽（考虑传入的宽度配置）
const calculateColumnWidths = () => {
  if (!scrollContainerRef.value) return;
  
  const rawWidth = scrollContainerRef.value.clientWidth;
  // 预留滚动条与舍入误差，按略小于 100% 分配，避免撑出横向滚动条
  const currentContainerWidth = Math.max(0, rawWidth - CONTAINER_WIDTH_RESERVE);
  if (currentContainerWidth === 0) {
    setTimeout(() => calculateColumnWidths(), 100);
    return;
  }
  
  containerWidth.value = rawWidth;
  
  // 先解析所有列的宽度配置
  props.columns.forEach((col, index) => {
    parsedColumnWidths[index] = parseColumnWidth(col.width);
  });
  
  // 分离像素列和百分比列（用户拖拽宽度优先）
  const pxColumns: Array<{ index: number; width: number }> = [];
  const percentColumns: Array<{ index: number; percent: number }> = [];
  const autoColumns: number[] = [];
  
  props.columns.forEach((col, index) => {
    if (userResizedWidths[index] !== undefined) {
      pxColumns.push({ index, width: userResizedWidths[index] });
      return;
    }
    const parsed = parsedColumnWidths[index];
    if (parsed) {
      if (parsed.type === 'px') {
        pxColumns.push({ index, width: parsed.value });
      } else if (parsed.type === 'percent') {
        percentColumns.push({ index, percent: parsed.value });
      }
    } else {
      autoColumns.push(index);
    }
  });
  
  // 计算像素列总宽度（使用设置的像素值，不强制最小宽度）
  const totalPxWidth = pxColumns.reduce((sum, col) => sum + col.width, 0);
  
  // 计算百分比列总百分比
  const totalPercent = percentColumns.reduce((sum, col) => sum + col.percent, 0);
  
  // 计算可用于百分比列分配的空间
  const availableWidth = Math.max(0, currentContainerWidth - totalPxWidth);
  
  // 计算百分比列的归一化系数（只有当总百分比超过100%时才归一化）
  const normalizeFactor = totalPercent > 0 ? (totalPercent > 100 ? 100 / totalPercent : 1) : 1;
  
  // 分配百分比列的宽度
  percentColumns.forEach(({ index, percent }) => {
    const normalizedPercent = percent * normalizeFactor;
    const width = (availableWidth * normalizedPercent) / 100;
    // 百分比列不强制最小宽度，完全按照百分比分配
    columnWidths[index] = width;
  });
  
  // 分配像素列的宽度（使用设置的像素值，不强制最小宽度）
  pxColumns.forEach(({ index, width }) => {
    columnWidths[index] = width;
  });
  
  // 计算百分比列已使用的宽度
  const totalPercentWidth = percentColumns.reduce((sum, { index }) => {
    return sum + (columnWidths[index] || 0);
  }, 0);
  
  // 计算剩余空间（容器宽度 - 像素列宽度 - 百分比列已使用的宽度）
  const remainingWidth = Math.max(0, currentContainerWidth - totalPxWidth - totalPercentWidth);
  
  // 对于没有配置宽度的列，均分剩余空间
  if (autoColumns.length > 0) {
    const autoColumnWidth = remainingWidth / autoColumns.length;
    autoColumns.forEach((index) => {
      columnWidths[index] = autoColumnWidth;
    });
  }
  
  // 计算表格总宽度，判断是否需要横向滚动（与容器真实宽度比较）
  const totalTableWidth = Object.values(columnWidths).reduce((sum, width) => sum + width, 0);
  needsHorizontalScroll.value = totalTableWidth > rawWidth && rawWidth > 0;
};

const updateHorizontalScrollFlag = () => {
  if (!scrollContainerRef.value) return;
  const currentContainerWidth = scrollContainerRef.value.clientWidth;
  const totalTableWidth = Object.values(columnWidths).reduce((sum, width) => sum + width, 0);
  needsHorizontalScroll.value = totalTableWidth > currentContainerWidth && currentContainerWidth > 0;
};

const getCurrentColumnWidth = (colIndex: number): number => {
  if (userResizedWidths[colIndex] !== undefined) return userResizedWidths[colIndex];
  if (columnWidths[colIndex] !== undefined) return columnWidths[colIndex];
  const headerEl = headerRefs[colIndex];
  if (headerEl) {
    const rect = headerEl.getBoundingClientRect();
    if (rect.width > 0) return rect.width;
  }
  return MIN_COLUMN_WIDTH;
};

const onResizePointerMove = (event: PointerEvent) => {
  if (!resizeState.value) return;
  event.preventDefault();

  // 节流：每帧最多更新一次，避免大表格拖拽时频繁触发响应式更新
  lastResizeClientX.value = event.clientX;
  needsOverflowRecheckAfterResize.value = true;

  if (resizeRafId.value !== null) return;
  resizeRafId.value = window.requestAnimationFrame(() => {
    resizeRafId.value = null;
    if (!resizeState.value || lastResizeClientX.value === null) return;

    const { colIndex, startX, startWidth } = resizeState.value;
    const deltaX = lastResizeClientX.value - startX;
    const nextWidth = Math.max(RESIZE_MIN_COLUMN_WIDTH, Math.round(startWidth + deltaX));

    userResizedWidths[colIndex] = nextWidth;
    columnWidths[colIndex] = nextWidth;
    updateHorizontalScrollFlag();
  });
};

const onResizePointerUp = () => {
  if (!isResizing.value) return;

  isResizing.value = false;
  activeResizeColIndex.value = null;
  resizeState.value = null;
  lastResizeClientX.value = null;

  if (resizeRafId.value !== null) {
    window.cancelAnimationFrame(resizeRafId.value);
    resizeRafId.value = null;
  }

  // 拖拽结束后再统一清理溢出缓存，避免拖拽过程中反复清理导致卡顿
  if (needsOverflowRecheckAfterResize.value) {
    needsOverflowRecheckAfterResize.value = false;
    clearOverflowCache();
  }

  // 全局兜底解绑：防止快速拖动时 pointerup 丢失导致“持续锁定”
  if (hasGlobalResizeEndListeners.value) {
    window.removeEventListener('pointerup', onResizePointerUp);
    window.removeEventListener('pointercancel', onResizePointerUp);
    window.removeEventListener('blur', onResizePointerUp);
    hasGlobalResizeEndListeners.value = false;
  }
};

const onResizePointerDown = (colIndex: number, event: PointerEvent) => {
  if (event.pointerType === 'mouse' && 'button' in event && (event as PointerEvent & { button: number }).button !== 0) {
    return;
  }
  // 双击时不进入拖拽（避免误触发）
  if (event.detail && event.detail > 1) return;

  const startWidth = getCurrentColumnWidth(colIndex);
  isResizing.value = true;
  activeResizeColIndex.value = colIndex;
  resizeState.value = { colIndex, startX: event.clientX, startWidth };
  needsOverflowRecheckAfterResize.value = false;

  // 全局兜底：即使在组件外释放，也能结束拖拽
  if (!hasGlobalResizeEndListeners.value) {
    window.addEventListener('pointerup', onResizePointerUp, { passive: true });
    window.addEventListener('pointercancel', onResizePointerUp, { passive: true });
    window.addEventListener('blur', onResizePointerUp, { passive: true });
    hasGlobalResizeEndListeners.value = true;
  }

  try {
    (event.currentTarget as HTMLElement | null)?.setPointerCapture?.(event.pointerId);
  } catch {
    // ignore
  }

};

// 计算表头宽度（简化版：固定最小150px，最大200px，优先按表头宽度）
const calculateHeaderWidths = debounce(() => {
  nextTick(() => {
    // 重新解析所有列的宽度配置（每次重新计算时都解析，确保配置变化时能生效）
    props.columns.forEach((col, index) => {
      parsedColumnWidths[index] = parseColumnWidth(col.width);
    });
    
    // 检查是否所有表头引用都已设置（仅对自动列需要）
    const allHeadersSet = props.columns.every((col, index) => {
      const parsed = parsedColumnWidths[index];
      // 如果列有配置宽度，不需要表头引用；否则需要
      return parsed !== null || headerRefs[index];
    });
    
    if (!allHeadersSet) {
      setTimeout(() => calculateHeaderWidths(), 50);
      return;
    }
    
    calculateColumnWidths();
  });
}, HEADER_WIDTH_DEBOUNCE_DELAY);

// 获取列样式 - 优先使用传入的宽度配置
const getColumnStyle = (col: TableColumn, colIndex: number, isCell: boolean = false): Record<string, string> => {
  const style: Record<string, string> = {
    textAlign: (isCell ? col.align : col.headerAlign) || 'left',
  };

  // 用户拖拽宽度优先
  if (userResizedWidths[colIndex] !== undefined) {
    const width = userResizedWidths[colIndex];
    style.width = `${width}px`;
    style.minWidth = `${width}px`;
    if (isCell) {
      style.maxWidth = `${width}px`;
      style.boxSizing = 'border-box';
    }
    return style;
  }
  
  // 如果列宽配置还没有被解析，立即解析
  if (parsedColumnWidths[colIndex] === undefined && col.width) {
    parsedColumnWidths[colIndex] = parseColumnWidth(col.width);
  }
  
  // 优先使用传入的宽度配置
  const parsed = parsedColumnWidths[colIndex];
  const calculatedWidth = columnWidths[colIndex] || MIN_COLUMN_WIDTH;
  
  if (parsed) {
    if (parsed.type === 'px') {
      // 像素值直接使用
      const width = parsed.value;
      if (!isCell) {
        style.width = `${width}px`;
        style.minWidth = `${width}px`;
      } else {
        style.width = `${width}px`;
        style.minWidth = `${width}px`;
        style.maxWidth = `${width}px`;
        style.boxSizing = 'border-box';
      }
    } else if (parsed.type === 'percent') {
      // 百分比值使用计算后的像素宽度（基于可用空间和百分比计算）
      if (!isCell) {
        style.width = `${calculatedWidth}px`;
        style.minWidth = `${calculatedWidth}px`;
      } else {
        style.width = `${calculatedWidth}px`;
        style.minWidth = `${calculatedWidth}px`;
        style.maxWidth = `${calculatedWidth}px`;
        style.boxSizing = 'border-box';
      }
    }
  } else {
    // 没有配置宽度，使用自动计算的宽度
    if (!isCell) {
      style.width = `${calculatedWidth}px`;
      style.minWidth = `${calculatedWidth}px`;
    } else {
      style.width = `${calculatedWidth}px`;
      style.minWidth = `${calculatedWidth}px`;
      style.maxWidth = `${calculatedWidth}px`;
      style.boxSizing = 'border-box';
    }
  }
  
  return style;
};

// 获取单元格值
const getCellValue = (col: TableColumn, row: TableData): any => {
  return (row as Record<string, any>)[col.key];
};


// 渲染单元格内容
const renderCell = (col: TableColumn, row: TableData): string => {
  const value = getCellValue(col, row);
  
  if (col.render) {
    return col.render(value, row);
  }
  
  // 只处理科学计数法，其他不做任何处理，保持服务端原始返回
  return convertScientificNotation(value);
};

// 获取tooltip内容（保留 HTML，用于 Tooltip 组件显示）
const getTooltipContent = (col: TableColumn, row: TableData): string => {
  const value = getCellValue(col, row);
  // 如果使用自定义渲染函数，直接返回（通常已经包含 HTML）
  if (col.render) {
    return col.render(value, row);
  }
  
  // 只处理科学计数法，其他不做任何处理
  let content = convertScientificNotation(value);
  
  // 检查内容是否已经包含 HTML 标签
  const hasHtmlTags = /<[^>]+>/.test(content);
  
  if (!hasHtmlTags) {
    // 纯文本内容：处理转义字符
    // 先转义 HTML 特殊字符，防止 XSS 攻击
    content = content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
    
    // 处理转义字符
    // 将换行符转换为 <br>
    content = content.replace(/\n/g, '<br>');
    // 将制表符转换为 4 个空格
    content = content.replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
    // 将连续空格转换为 &nbsp;（保留空格显示）
    content = content.replace(/ {2,}/g, (match) => {
      return '&nbsp;'.repeat(match.length - 1) + ' ';
    });
  }
  // 如果内容已经包含 HTML，直接返回（假设已经正确处理了转义字符）
  
  return content;
};

// 组件挂载时添加滚动事件监听和计算表头宽度
onMounted(() => {
  nextTick(() => {
    if (scrollContainerRef.value) {
      // 监听容器大小变化，重新计算列宽
      resizeObserverRef.value = new ResizeObserver(() => {
        calculateHeaderWidths();
      });
      resizeObserverRef.value.observe(scrollContainerRef.value);
    }
    // 计算表头宽度
    calculateHeaderWidths();
  });
});

// 组件卸载时移除滚动事件监听和清理资源
onUnmounted(() => {
  onResizePointerUp();
  
  // 清理 ResizeObserver
  if (resizeObserverRef.value) {
    resizeObserverRef.value.disconnect();
    resizeObserverRef.value = null;
  }
  
  // 清理防抖定时器
  overflowDebounceTimers.forEach(timer => {
    if (timer) {
      window.clearTimeout(timer);
    }
  });
  overflowDebounceTimers.clear();
  
  // 清理缓存
  overflowCache.clear();
});
</script>

<style scoped>
/* 表格容器基础字体大小，使用相对单位 rem，跟随系统字体大小 */
.bg-white.rounded-lg {
  font-size: 0.875rem; /* 14px，基于浏览器默认字体大小 16px */
}

/* 移动端列标题样式 */
.mobile-col-title {
  font-size: 1em;
}

/* 移动端列内容样式 */
.mobile-col-content {
  font-size: 1em;
}

/* 表格样式 */
:deep(table) {
  @apply border-collapse m-0;
  border-spacing: 0;
  font-size: 1em; /* 继承父元素字体大小 */
}

:deep(table.table-fixed) {
  table-layout: fixed !important; /* 固定布局，数据列严格遵循表头宽度 */
  width: auto; /* 表格宽度根据列宽自适应，可以超出容器 */
  min-width: 100%; /* 最小宽度占满容器 */
}

/* 不使用固定布局时，让表格自适应容器宽度 */
:deep(table:not(.table-fixed)) {
  table-layout: auto;
  width: 100%; /* 表格宽度占满容器 */
  max-width: 100%; /* 确保不超过容器宽度 */
}

:deep(thead.sticky) {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
}

:deep(th) {
  @apply px-3 py-1.5 font-normal align-middle;
  overflow: visible;
  font-size: 1em; /* 使用相对单位 em，继承父元素字体大小 */
  white-space: nowrap; /* 表头单行显示，不换行 */
  box-sizing: border-box; /* 确保 padding 包含在宽度内 */
  /* 宽度由 JavaScript 动态计算并设置 */
}

:deep(td) {
  @apply px-3 py-1 align-middle leading-tight;
  overflow: hidden;
  font-size: 1em; /* 使用相对单位 em，继承父元素字体大小 */
  box-sizing: border-box; /* 确保 padding 包含在宽度内 */
  /* 数据列宽度严格遵循表头宽度，由 JavaScript 动态设置 */
  word-wrap: break-word; /* 允许长文本换行 */
  word-break: break-all; /* 允许在任意字符处换行 */
}

/* 表头行样式 - 表头下方使用1px分割线，白色背景，与数据行分割线颜色一致 */
:deep(thead tr) {
  border-bottom-width: 1px !important;
  border-bottom-color: rgb(229, 231, 235) !important; /* gray-200，与数据行一致 */
  background-color: white !important;
}

/* 表头单元格样式 - 字体加粗，文字颜色更深，白色背景 */
:deep(thead th) {
  background-color: white !important;
  font-weight: 600 !important;
  color: rgb(55, 65, 81) !important; /* gray-700 */
  padding-top: 0.75rem !important; /* py-3 */
  padding-bottom: 0.75rem !important;
}

/* 数据行样式 - 每行都有分割线，包括最后一行 */
:deep(tbody tr) {
  border-bottom-width: 1px !important;
  border-bottom-color: rgb(229, 231, 235) !important; /* gray-200 */
  background-color: white;
  transition: background-color 0.15s ease;
}

:deep(tbody tr:hover) {
  background-color: rgb(249, 250, 251) !important; /* gray-50 */
}

/* 确保最后一行也有分割线 */
:deep(tbody tr:last-child) {
  border-bottom-width: 1px !important;
  border-bottom-color: rgb(229, 231, 235) !important; /* gray-200 */
}

/* 表格单元格样式 - 允许 tooltip 溢出 */
:deep(.table-cell-with-tooltip) {
  overflow: visible !important;
  position: relative;
}

/* 单元格内容样式 */
.cell-content {
  position: relative;
  min-width: 0;
  width: 100%;
}

/* 移动端单元格内容样式 */
.cell-content-mobile {
  position: relative;
  min-width: 0;
  width: 100%;
  word-break: break-word;
  overflow-wrap: break-word;
  /* 移动端允许文本换行，不强制单行显示 */
}

/* 确保 Select 下拉菜单在分享页面等高 z-index 环境下正常显示 */
:deep([data-radix-select-content]) {
  z-index: 10000 !important;
}

:deep([data-radix-popper-content-wrapper]) {
  z-index: 10000 !important;
}

/* Tooltip 内容换行样式 */
:deep([data-radix-tooltip-content]) {
  white-space: normal !important;
  word-wrap: break-word !important;
  overflow-wrap: break-word !important;
  max-width: 28rem; /* max-w-md */
}

:deep([data-radix-tooltip-content] > div) {
  white-space: normal !important;
  word-wrap: break-word !important;
  overflow-wrap: break-word !important;
}
/* 分割线拖拽体验：hover 时增强可见性 */
.column-resizer {
  opacity: 0;
  pointer-events: none;
  transition: opacity 120ms ease;
}

/* 鼠标移入表头区域才显示可拖拽分割线 */
:deep(thead:hover) .column-resizer {
  opacity: 1;
  pointer-events: auto;
}

/* 表头 hover 时显示竖向分割线（右边框） */
:deep(thead:hover th) {
  border-right-color: rgb(229, 231, 235); /* gray-200 */
}

/* 表头 hover 时，分割线线条可见（不影响布局） */
:deep(thead:hover) .resizer-line {
  background-color: rgb(229, 231, 235); /* gray-200 */
}

.column-resizer:hover .resizer-line {
  background-color: rgb(156, 163, 175); /* gray-400 */
}

.column-resizer.is-active .resizer-line {
  background-color: rgb(0, 0, 0); /* black */
  width: 2px;
}

/* 整列选中（右侧竖线高亮），用 inset shadow 避免边框宽度导致错位 */
:deep(th.col-resizing) {
  border-right-color: transparent !important;
  box-shadow: inset -2px 0 0 rgb(0, 0, 0);
}

/* 拖拽中即便移出表头也保持可见 */
.column-resizer.is-active {
  opacity: 1;
  pointer-events: auto;
}

/* 拖拽期间：在组件范围内固定光标、禁止选择（避免原生 body 操作） */
:deep(.select-none) {
  cursor: col-resize;
}

:deep(.select-none *) {
  cursor: col-resize;
}
</style>

