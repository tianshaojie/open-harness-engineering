<script setup lang="ts">
import { DropdownMenuRoot } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  class?: string
  defaultOpen?: boolean
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

const props = withDefaults(defineProps<Props>(), {
  defaultOpen: false
})
</script>

<template>
  <DropdownMenuRoot
    :default-open="defaultOpen"
    :open="open"
    :on-open-change="onOpenChange"
    :class="cn('relative', props.class)"
  >
    <slot />
  </DropdownMenuRoot>
</template>

<style scoped>
:deep([data-radix-popper-content-wrapper]) {
  z-index: 50;
}
</style>
