<script setup lang="ts">
import { DialogRoot } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <DialogRoot :class="cn('', props.class)">
    <slot />
  </DialogRoot>
</template>
