<script setup lang="ts">
import { DropdownMenuSub as RadixDropdownMenuSub } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  class?: string
  defaultOpen?: boolean
  open?: boolean
  onOpenChange?: (open: boolean) => void
}>(), {
  defaultOpen: false
})
</script>

<template>
  <RadixDropdownMenuSub
    :default-open="defaultOpen"
    :open="open"
    :on-open-change="onOpenChange"
    :class="cn('', props.class)"
  >
    <slot />
  </RadixDropdownMenuSub>
</template>
