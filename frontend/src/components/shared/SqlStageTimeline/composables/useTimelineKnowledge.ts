/**
 * Timeline 知识库相关逻辑 Composable
 */
import { computed, unref, type MaybeRef } from 'vue';
import type { SqlStageStateItem } from '@/views/chat/types';
import type { KnowledgeItem, KnowledgeMetadata } from '../types';

/**
 * 构建知识库原文查看链接
 */
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

const resolveKnowledgeHost = (item: Record<string, unknown>): string => {
  const targetEnv = normalizeRuntimeEnv(item.target_env);
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

const getKnowledgeBaseLink = (item: Record<string, unknown>): string | undefined => {
  const { data_id, file_id, knowledge_code } = item;

  if (!data_id || !file_id || !knowledge_code) {
    return undefined;
  }
  const host = resolveKnowledgeHost(item);
  return `${host}/#/system/knowledge-base/${encodeURIComponent(String(knowledge_code))}/files/${encodeURIComponent(String(file_id))}?data_id=${encodeURIComponent(String(data_id))}`;
};

/**
 * 获取知识库项目标题
 */
const getKnowledgeTitle = (item: KnowledgeItem): string => {
  const type = item.type as string;
  if (type === 'qa' || type === 'liked') {
    return (item.question || item.title || item.content_preview || '暂无标题') as string;
  } else if (type === 'table' || type === 'column') {
    return (item.name || item.title || '暂无名称') as string;
  } else if (type === 'dsl') {
    return (item.name || item.title || '暂无名称') as string;
  } else {
    return (item.title || item.name || item.content_preview || '暂无内容') as string;
  }
};

/**
 * 获取知识库类型样式类
 */
const getKnowledgeTypeClass = (type: string): string => {
  if (type === 'qa' || type === 'liked') {
    return 'bg-blue-100 text-blue-800';
  }
  if (type === 'liked') {
    return 'bg-purple-100 text-purple-800';
  }
  if (type === 'dsl') {
    return 'bg-green-100 text-green-800';
  }
  if (type === 'table' || type === 'column') {
    return 'bg-yellow-100 text-yellow-800';
  }
  return 'bg-gray-100 text-gray-800';
};

/**
 * 获取阶段的唯一 key
 */
const getStageToggleKey = (stage: SqlStageStateItem, indexHint?: number): string => {
  if (stage.stageId && stage.stageId.trim().length > 0) {
    return stage.stageId;
  }
  if (typeof indexHint === 'number') {
    return `${stage.key}-${indexHint}`;
  }
  return `${stage.key}-${stage.order ?? ''}`;
};

/**
 * 从阶段数据中提取知识库详情
 */
const getKnowledgeDetailsFromStage = (stage: SqlStageStateItem): KnowledgeItem[] => {
  const metadata = (stage.metadata ?? {}) as KnowledgeMetadata;

  if (Array.isArray(metadata.knowledge_details)) {
    return metadata.knowledge_details;
  }

  if (Array.isArray(metadata.knowledgeDetails)) {
    return metadata.knowledgeDetails;
  }

  const enriched = metadata.enriched;
  const libraries = enriched?.knowledgeDetails?.libraries;
  if (Array.isArray(libraries)) {
    const items: KnowledgeItem[] = [];
    libraries.forEach((library) => {
      const docs = library.filtered_recalled_documents || library.recalled_documents || [];
      docs.forEach((doc: KnowledgeItem, index: number) => {
        items.push({
          ...doc,
          type: doc.type || library.type,
          index: doc.index ?? index + 1,
        });
      });
    });
    return items;
  }

  return [];
};

/**
 * 使用知识库相关功能的 Composable
 */
export function useTimelineKnowledge(stages: MaybeRef<readonly SqlStageStateItem[]>) {
  /**
   * 知识库详情映射（缓存结果）
   */
  const knowledgeDetailsMap = computed(() => {
    const map = new Map<string, KnowledgeItem[]>();
    const stagesValue = unref(stages);
    stagesValue.forEach((stage, index) => {
      const key = getStageToggleKey(stage, index);
      const details = getKnowledgeDetailsFromStage(stage);
      map.set(key, details);
    });
    return map;
  });

  /**
   * 获取指定阶段的知识库详情
   */
  const getKnowledgeDetails = (stage: SqlStageStateItem, index?: number): KnowledgeItem[] => {
    const key = getStageToggleKey(stage, index ?? -1);
    return knowledgeDetailsMap.value.get(key) ?? [];
  };

  /**
   * 生成知识库项目的唯一 key
   */
  const getKnowledgeItemKey = (prefix: string, idx: number | string): string => {
    return `${prefix}-item-${idx}`;
  };

  return {
    getKnowledgeDetails,
    getKnowledgeItemKey,
    getKnowledgeBaseLink,
    getKnowledgeTitle,
    getKnowledgeTypeClass,
    getStageToggleKey,
  };
}
