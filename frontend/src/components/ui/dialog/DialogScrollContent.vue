<script setup lang="ts">
import { DialogContent as DialogContentRoot } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <DialogContentRoot
    :class="
      cn(
        'overflow-y-auto',
        props.class,
      )"
  >
    <slot />
  </DialogContentRoot>
</template>
