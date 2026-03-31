<script setup lang="ts">
import { DropdownMenuRadioItem as RadixDropdownMenuRadioItem } from 'radix-vue'
import { Circle } from 'lucide-vue-next'
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  class?: string
  value: string
  disabled?: boolean
}>(), {
  disabled: false
})
</script>

<template>
  <RadixDropdownMenuRadioItem
    :class="cn(
      'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      props.class
    )"
    :value="value"
    :disabled="disabled"
  >
    <span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <Circle class="h-2 w-2 fill-current" />
    </span>
    <slot />
  </RadixDropdownMenuRadioItem>
</template>
