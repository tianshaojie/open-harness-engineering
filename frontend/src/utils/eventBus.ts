import mitt from 'mitt';

// 定义事件类型
export enum EventTypes {
  AGENT_SELECTED = 'agent-selected',
  CHAT_MESSAGE = 'chat-message',
  NEED_RELOAD_HISTORY = 'need-reload-history',
  SCROLL_TO_BOTTOM = 'scroll-to-bottom',
  CHART_DATA_UPDATED = 'chart-data-updated',
  DATA_EXTRACTION_UPDATED = 'data-extraction-updated',
  CHART_PRELOAD = 'chart-preload',
  CONTENT_RENDERED = 'content-rendered'
}

// 统一的滚动事件参数类型
export interface ScrollToBottomEvent {
  // 滚动触发来源（与 useScrollManager 中优先级、分支一致）
  source?:
    | 'user'
    | 'system'
    | 'reasoning'
    | 'text'
    | 'stream_start'
    | 'confidence'
    | 'stage_finalize'
    | 'stage_snapshot'
    | 'stage_update';
  // 是否需要强制滚动（不考虑用户滚动状态）
  forceScroll?: boolean;
}

// 定义事件数据类型
export interface AgentSelectedEvent {
  agent: {
    name: string;
    display_name?: string;
    description: string;
    avatar?: string;
    color?: string;
    model?: string;
  };
  index?: number;
}

// 定义事件数据类型
export interface ChartDataUpdatedEvent {
  chartSuggestions: any[] | null;
  isPreloading?: boolean;
}

// 定义事件数据类型
export interface DataExtractionUpdatedEvent {
  userData: any[] | null;
  columns?: string[] | null;
}

// 定义预加载事件数据类型
export interface ChartPreloadEvent {
  isPreloading: boolean;
  userData?: any[] | null;
}

// 定义内容渲染完成事件数据类型
export interface ContentRenderedEvent {
  type: 'text' | 'markdown' | 'chart';
  messageId?: string;
  contentLength?: number;
  isFirstRender?: boolean;
}

// 创建事件总线
const eventBus = mitt();

export default eventBus; 