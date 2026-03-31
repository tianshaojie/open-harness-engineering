<template>
  <div class="flex flex-col items-center">
      <!-- 自定义图标或默认图标 -->
      <component
        :is="iconComponent"
        :class="[
          iconSize === 'sm' ? 'w-8 h-8 md:w-8 md:h-8' : '',
          iconSize === 'md' ? 'w-12 h-12 md:w-12 md:h-12' : '',
          iconSize === 'lg' ? 'w-16 h-16 md:w-16 md:h-16' : '',
          iconClass,
          iconColorClass
        ]"
      />
      
      <!-- 标题 -->
      <div class="text-gray-400 text-sm md:text-sm mb-2">{{ title }}</div>
      
      <!-- 描述 -->
      <div v-if="description" class="text-gray-400 text-xs md:text-xs mb-4 max-w-md">{{ description }}</div>
      
      <!-- 操作按钮插槽 -->
      <div v-if="$slots.action" class="mt-4">
        <slot name="action"></slot>
      </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { EmptyStateIcon } from '@/assets/svg-icon';
import type { Component } from 'vue';

interface Props {
  /** 空状态标题 */
  title?: string;
  /** 空状态描述 */
  description?: string;
  /** 自定义图标组件 */
  icon?: Component | string;
  /** 自定义图标类名 */
  iconClass?: string;
  /** 图标颜色（Tailwind 类名，如 text-gray-400） */
  iconColor?: string;
  /** 图标大小 */
  iconSize?: 'sm' | 'md' | 'lg';
}

const props = withDefaults(defineProps<Props>(), {
  title: '暂无数据',
  description: '',
  icon: '',
  iconClass: '',
  iconColor: 'text-gray-300',
  iconSize: 'md',
});

// 计算图标组件
const iconComponent = computed(() => {
  return props.icon || EmptyStateIcon;
});

// 计算图标颜色类名
const iconColorClass = computed(() => {
  return props.iconColor || 'text-gray-300';
});
</script>

