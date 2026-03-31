<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div
    :class="cn('overflow-hidden p-1 text-foreground', props.class)"
    v-bind="$attrs"
  >
    <slot />
  </div>
</template>
