<script setup lang="ts">
import { SelectContent, SelectViewport, SelectScrollUpButton, SelectScrollDownButton, SelectPortal } from 'radix-vue'
import { cn } from '@/lib/utils'
import { ChevronUp, ChevronDown } from 'lucide-vue-next'

const props = withDefaults(defineProps<{
  class?: string
  position?: 'popper' | 'item-aligned'
  side?: 'top' | 'right' | 'bottom' | 'left'
  align?: 'start' | 'center' | 'end'
  sideOffset?: number
}>(), {
  position: 'popper',
  side: 'bottom',
  align: 'start',
  sideOffset: 4
})
</script>

<template>
  <SelectPortal>
    <SelectContent
      :class="cn(
        'relative z-50 max-h-96 overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 w-[var(--radix-select-trigger-width)]',
        props.class
      )"
      :position="position"
      :side="side"
      :align="align"
      :side-offset="sideOffset"
    >
      <SelectScrollUpButton
        class="flex cursor-default items-center justify-center py-1"
      >
        <ChevronUp class="h-4 w-4" />
      </SelectScrollUpButton>
      <SelectViewport
        class="p-1"
      >
        <slot />
      </SelectViewport>
      <SelectScrollDownButton
        class="flex cursor-default items-center justify-center py-1"
      >
        <ChevronDown class="h-4 w-4" />
      </SelectScrollDownButton>
    </SelectContent>
  </SelectPortal>
</template>
