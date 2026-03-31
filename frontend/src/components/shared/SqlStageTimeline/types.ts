/**
 * SqlStageTimeline 组件类型定义
 */
import type { SqlStageStateItem, SqlStageStatus } from '@/views/chat/types';
import type { MessageExecutionStatus } from '@/api/types/chat';

/**
 * Timeline 组件常量配置
 */
export const TIMELINE_CONFIG = {
  /** 定时器更新间隔（毫秒） */
  UPDATE_INTERVAL: 200,
  /** 自动折叠延迟时间（毫秒） */
  AUTO_COLLAPSE_DELAY: 3000,
  /** JSON 预览最大长度 */
  JSON_PREVIEW_LENGTH: 200,
  /** JSON 预览短文本最大长度 */
  JSON_PREVIEW_SHORT_LENGTH: 80,
} as const;

/**
 * 知识库项目类型定义
 */
export interface KnowledgeItem {
  type?: string;
  index?: number;
  score?: number | string;
  question?: string;
  title?: string;
  name?: string;
  content_preview?: string;
  [key: string]: unknown;
}

/**
 * 知识库元数据类型定义
 */
export interface KnowledgeMetadata {
  knowledge_details?: KnowledgeItem[];
  knowledgeDetails?: KnowledgeItem[];
  enriched?: {
    knowledgeDetails?: {
      libraries?: Array<{
        type?: string;
        filtered_recalled_documents?: KnowledgeItem[];
        recalled_documents?: KnowledgeItem[];
      }>;
    };
    filteringSteps?: Array<{
      stepKey: string;
      stepName: string;
      count: number;
      description?: string;
      knowledgeList?: KnowledgeItem[];
    }>;
  };
}

/**
 * 消息状态类型
 */
export type MessageStatus = 'loading' | 'success' | 'failed' | 'pending' | 'processing' | undefined;

/**
 * Timeline 组件 Props 接口
 */
export interface TimelineProps {
  /** 必需：阶段数据数组 */
  stages: SqlStageStateItem[];
  /** 可选：消息ID，用于生成唯一的子组件标识 */
  messageId?: string | number;
  /** 可选：是否自动折叠（成功后3秒自动折叠），默认 true */
  autoCollapse?: boolean;
  /** 可选：自动折叠延迟时间（毫秒），默认 3000 */
  autoCollapseDelay?: number;
  /** 可选：默认是否折叠，默认 false */
  defaultCollapsed?: boolean;
  /** 可选：是否显示折叠头部，默认 true */
  showCollapseHeader?: boolean;
  /** 可选：消息整体状态（用于流式阶段保持"进行中"），默认 'loading' */
  messageStatus?: MessageStatus;
  /** 可选：后端给出的最终整体状态 */
  finalStatus?: SqlStageStatus | string | null;
  /** 可选：是否有 SQL（用于判断是否自动展开最后一个节点），默认 true */
  hasSql?: boolean;
  /** 可选：后端执行结果（1-成功，0-失败），用于准确判断整体状态 */
  execRes?: number;
  /** 可选：后端细粒度执行状态 */
  executionStatus?: MessageExecutionStatus | null;
  /** 可选：是否已收到后端 done 标记，默认 false */
  stagesFinalized?: boolean;
  /** 可选：是否显示单节点超时提示（历史消息传 false），默认 true */
  showTimeoutHint?: boolean;
}

/**
 * Timeline 组件 Emits 接口
 */
export interface TimelineEmits {
  /** 重试失败阶段（预留功能，目前组件内部未触发） */
  (e: 'retry', stage: SqlStageStateItem): void;
  /** 折叠状态变化 */
  (e: 'toggle-collapse', collapsed: boolean): void;
}

