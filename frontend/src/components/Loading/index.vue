<template>
  <div :class="containerClass">
    <!-- 加载动画 -->
    <div v-if="type === 'spinner'" class="mb-4">
      <div class="animate-spin rounded-full h-8 w-8 md:h-8 md:w-8 border-b-2 border-indigo-500"></div>
    </div>
    
    <!-- 点状加载动画 -->
    <div v-else-if="type === 'dots'" class="flex items-center gap-1.5">
      <div class="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground"></div>
      <div class="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0.2s]"></div>
      <div class="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:0.4s]"></div>
    </div>
    
    <!-- 加载文本 -->
    <p v-if="text" class="text-sm md:text-sm text-gray-400">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  /** 加载动画类型 */
  type?: 'spinner' | 'dots';
  /** 加载文本 */
  text?: string;
  /** 容器类名 */
  containerClass?: string;
}

withDefaults(defineProps<Props>(), {
  type: 'spinner',
  text: '',
  containerClass: 'flex flex-col items-center text-gray-400'
});
</script>

