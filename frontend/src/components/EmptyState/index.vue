<template>
  <!-- 紧凑模式：用于加载更多等场景 -->
  <div v-if="mode === 'compact'" :class="compactContainerClass">
    <!-- 没有更多状态 -->
    <div v-if="hasMore === false" class="text-gray-500 text-sm">
      {{ endText }}
    </div>
    
    <!-- 加载状态 -->
    <div v-else-if="loading" class="flex items-center justify-center text-gray-600 text-sm">
      <div class="flex items-center justify-center mr-2">
        <LoadingIcon class="w-4 h-4 text-indigo-500 animate-spin" />
      </div>
      <span>{{ loadingText }}</span>
    </div>
  </div>

  <!-- 全屏模式：用于空数据场景 -->
  <section v-else class="flex flex-col items-center justify-center h-full p-8 md:p-8 text-center">
    <Loading v-if="loading" :text="loadingText" />
    <Empty 
      v-else
      :title="title"
      :description="description"
      :icon="icon"
      :icon-class="iconClass"
      :icon-color="iconColor"
      :icon-size="iconSize"
    >
      <template v-if="$slots.action" #action>
        <slot name="action"></slot>
      </template>
    </Empty>
  </section>
</template>

<script setup lang="ts">
import Loading from '@/components/Loading/index.vue';
import Empty from '@/components/Empty/index.vue';
import { LoadingIcon } from '@/assets/svg-icon';

interface Props {
  /** 布局模式：compact（紧凑，用于加载更多）| fullscreen（全屏，用于空数据） */
  mode?: 'compact' | 'fullscreen';
  /** 是否显示加载状态 */
  loading?: boolean;
  /** 加载状态文本 */
  loadingText?: string;
  /** 是否还有更多数据（仅 compact 模式有效） */
  hasMore?: boolean;
  /** 没有更多数据时的文本（仅 compact 模式有效） */
  endText?: string;
  /** 空状态标题 */
  title?: string;
  /** 空状态描述 */
  description?: string;
  /** 自定义图标 URL（使用 ?url 导入的 SVG） */
  icon?: string;
  /** 自定义图标类名 */
  iconClass?: string;
  /** 图标颜色 */
  iconColor?: string;
  /** 图标大小 */
  iconSize?: 'sm' | 'md' | 'lg';
  /** 紧凑模式容器类名 */
  compactContainerClass?: string;
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'fullscreen',
  loading: false,
  loadingText: '正在加载...',
  hasMore: undefined,
  endText: '已经到顶了',
  title: '暂无数据',
  description: '',
  icon: '',
  iconClass: '',
  iconColor: 'currentColor',
  iconSize: 'md',
  compactContainerClass: 'p-3 text-center',
});
</script>
