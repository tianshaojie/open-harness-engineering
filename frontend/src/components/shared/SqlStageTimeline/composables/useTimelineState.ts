/**
 * Timeline 状态管理 Composable
 */
import { ref, watch, unref, type MaybeRef } from 'vue';
import type { SqlStageStateItem } from '@/views/chat/types';

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
 * 使用 Timeline 状态管理的 Composable
 */
export function useTimelineState(
  stages: MaybeRef<readonly SqlStageStateItem[]>,
  defaultCollapsed: boolean,
  hasSql: MaybeRef<boolean>,
  stagesFinalized: MaybeRef<boolean>
) {
  // 折叠状态
  const isCollapsed = ref(defaultCollapsed);

  // 每个阶段的展开状态
  const stageExpandStates = ref<Record<string, boolean>>({});

  // 统一管理展开/折叠状态
  const expandedKnowledgeItems = ref<Record<string, boolean>>({});
  const expandedFilteringSteps = ref<Record<string, boolean>>({});
  const expandedDetailSections = ref<Record<string, boolean>>({});

  /**
   * 切换节点详情展开
   */
  const toggleStage = (key: string) => {
    const current = stageExpandStates.value[key];
    stageExpandStates.value = {
      ...stageExpandStates.value,
      [key]: !current,
    };
  };

  /**
   * 切换知识库项目展开
   */
  const toggleKnowledgeItem = (key: string | number) => {
    const id = String(key);
    expandedKnowledgeItems.value[id] = !expandedKnowledgeItems.value[id];
  };

  const isKnowledgeItemExpanded = (key: string | number): boolean => {
    return !!expandedKnowledgeItems.value[String(key)];
  };

  /**
   * 切换过滤步骤展开
   */
  const toggleFilteringStep = (key: string | number) => {
    const id = String(key);
    expandedFilteringSteps.value[id] = !expandedFilteringSteps.value[id];
  };

  const isFilteringStepExpanded = (key: string | number): boolean => {
    return !!expandedFilteringSteps.value[String(key)];
  };

  /**
   * 切换详情区域展开
   */
  const toggleDetailSection = (key: string) => {
    expandedDetailSections.value[key] = !expandedDetailSections.value[key];
  };

  const isSectionExpanded = (key: string): boolean => {
    return !!expandedDetailSections.value[key];
  };

  /**
   * 切换折叠状态
   */
  const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value;
  };

  /**
   * 初始化阶段展开状态
   * 只初始化新出现的阶段，不覆盖用户已手动设置的状态
   * 默认所有阶段都折叠，只在流式结束时或历史消息中展开最后一个阶段（无SQL场景）
   */
  const initStageExpandStates = () => {
    const newStates = { ...stageExpandStates.value };
    const stagesValue = unref(stages);

    if (!stagesValue || stagesValue.length === 0) {
      return;
    }

    const finalized = unref(stagesFinalized);

    stagesValue.forEach((stage, index) => {
      const toggleKey = getStageToggleKey(stage, index);
      // 如果阶段已存在（用户可能已手动展开/折叠），则保持当前状态
      if (toggleKey in newStates) {
        return;
      }

      // 最终节点（最后一个阶段）在 finalized 时默认展开
      const isLastStage = index === stagesValue.length - 1;
      if (finalized && isLastStage) {
        newStates[toggleKey] = true;
      } else {
        // 新阶段：默认全部折叠
        newStates[toggleKey] = false;
      }
    });

    stageExpandStates.value = newStates;
  };

  /**
   * 在阶段完成时自动展开最终节点（最后一个阶段）
   */
  const expandLastFailedStage = () => {
    const stagesValue = unref(stages);
    if (!stagesValue || stagesValue.length === 0) {
      return;
    }

    const lastStage = stagesValue[stagesValue.length - 1];
    if (!lastStage) {
      return;
    }

    stageExpandStates.value = {
      ...stageExpandStates.value,
      [getStageToggleKey(lastStage, stagesValue.length - 1)]: true,
    };
  };

  // 监听 stages 变化，初始化展开状态
  // 使用 shallow 监听，避免 stages 内部属性变化时重复初始化
  watch(
    () => unref(stages),
    (newStages, oldStages) => {
      if (!newStages || newStages.length === 0) {
        return;
      }
      // 只在 stages 数组长度变化或阶段 key 变化时初始化（避免内部属性变化触发）
      const newKeys = newStages.map((s, i) => getStageToggleKey(s, i)).join(',');
      const oldKeys = oldStages ? oldStages.map((s, i) => getStageToggleKey(s, i)).join(',') : '';
      if (newKeys !== oldKeys) {
        initStageExpandStates();
      }
    },
    { immediate: true }
  );

  // 监听 stagesFinalized，自动展开最终节点
  // 使用 immediate: true 确保历史消息（初始化时就是 finalized）也能触发
  watch(
    () => unref(stagesFinalized),
    (finalized) => {
      if (finalized) {
        expandLastFailedStage();
      }
    },
    { immediate: true }
  );

  // 移除阶段状态监听，只依赖 stagesFinalized 来触发展开
  // 这样可以避免流式过程中频繁触发展开逻辑

  return {
    isCollapsed,
    stageExpandStates,
    expandedKnowledgeItems,
    expandedFilteringSteps,
    expandedDetailSections,
    toggleStage,
    toggleKnowledgeItem,
    isKnowledgeItemExpanded,
    toggleFilteringStep,
    isFilteringStepExpanded,
    toggleDetailSection,
    isSectionExpanded,
    toggleCollapse,
    initStageExpandStates,
    expandLastFailedStage,
  };
}

