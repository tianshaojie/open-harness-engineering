<script setup lang="ts">
import { ToastTitle as ToastTitleRoot } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <ToastTitleRoot
    :class="
      cn(
        'text-sm font-semibold',
        props.class,
      )"
  >
    <slot />
  </ToastTitleRoot>
</template>
