/**
 * Timeline 定时器逻辑 Composable
 */
import { ref, computed, watch, onUnmounted, unref, type MaybeRef } from 'vue';
import type { SqlStageStateItem } from '@/views/chat/types';
import { TIMELINE_CONFIG } from '../types';

/**
 * 使用 Timeline 定时器的 Composable
 */
export function useTimelineTiming(stages: MaybeRef<readonly SqlStageStateItem[]>) {
  // 当前时间（用于动态计算耗时）
  const currentTime = ref(Date.now());
  
  let updateTimer: ReturnType<typeof setInterval> | null = null;
  let isMounted = true;

  /**
   * 检查是否有正在进行中的阶段
   */
  const hasProcessingStage = computed(() => {
    const stagesValue = unref(stages);
    return stagesValue.some(stage => stage.status === 'processing');
  });

  /**
   * 获取阶段的实时耗时
   * 对于正在进行中的阶段，动态计算耗时
   * 对于已完成的阶段，返回后端传来的 elapsedTime
   */
  const getStageElapsedTime = (stage: SqlStageStateItem): number | undefined => {
    // 如果阶段已完成（有 elapsedTime），直接返回
    if (stage.elapsedTime !== undefined && stage.elapsedTime !== null) {
      return stage.elapsedTime;
    }

    // 如果阶段正在进行中且有 startTime，动态计算耗时
    if (stage.status === 'processing' && stage.startTime) {
      // startTime 是时间戳（秒），currentTime.value 是毫秒
      const elapsedMs = currentTime.value - (stage.startTime * 1000);
      return elapsedMs / 1000; // 转换为秒
    }

    return undefined;
  };

  /**
   * 总耗时（包含动态计算的正在进行中的阶段）
   */
  const totalElapsedTime = computed(() => {
    let total = 0;
    const stagesValue = unref(stages);
    stagesValue.forEach(stage => {
      const elapsed = getStageElapsedTime(stage);
      if (elapsed !== undefined) {
        total += elapsed;
      }
    });
    return total;
  });

  /**
   * 启动定时器更新当前时间（用于动态计算耗时）
   */
  const startUpdateTimer = () => {
    if (updateTimer) {
      clearInterval(updateTimer);
    }
    updateTimer = setInterval(() => {
      // 只有在组件仍然挂载时才更新
      if (isMounted) {
        currentTime.value = Date.now();
      }
    }, TIMELINE_CONFIG.UPDATE_INTERVAL);
  };

  /**
   * 停止定时器
   */
  const stopUpdateTimer = () => {
    if (updateTimer) {
      clearInterval(updateTimer);
      updateTimer = null;
    }
  };

  // 监听是否有正在进行中的阶段，动态启停定时器
  watch(hasProcessingStage, (hasProcessing) => {
    // 只有在组件仍然挂载时才启动定时器
    if (!isMounted) {
      return;
    }
    if (hasProcessing) {
      startUpdateTimer();
    } else {
      stopUpdateTimer();
    }
  }, { immediate: true });

  // 组件卸载时清理定时器
  onUnmounted(() => {
    isMounted = false;
    stopUpdateTimer();
  });

  return {
    currentTime,
    getStageElapsedTime,
    totalElapsedTime,
    startUpdateTimer,
    stopUpdateTimer,
  };
}

