<script setup lang="ts">
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  class?: string
  overflowX?: 'auto' | 'hidden' | 'visible'
}>(), {
  overflowX: 'auto'
})
</script>

<template>
  <div 
    class="relative w-full"
    :class="{
      'overflow-auto': overflowX === 'auto',
      'overflow-x-hidden overflow-y-auto': overflowX === 'hidden',
      'overflow-visible': overflowX === 'visible'
    }"
  >
    <table :class="cn('w-full caption-bottom text-sm', props.class)">
      <slot />
    </table>
  </div>
</template> 