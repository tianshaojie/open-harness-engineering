<script setup lang="ts">
import { DropdownMenuCheckboxItem as RadixDropdownMenuCheckboxItem } from 'radix-vue'
import { Check } from 'lucide-vue-next'
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  class?: string
  checked?: boolean
  disabled?: boolean
  onCheckedChange?: (checked: boolean) => void
}>(), {
  checked: false,
  disabled: false
})
</script>

<template>
  <RadixDropdownMenuCheckboxItem
    :class="cn(
      'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      props.class
    )"
    :checked="checked"
    :disabled="disabled"
    :on-checked-change="onCheckedChange"
  >
    <span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <Check class="h-4 w-4" />
    </span>
    <slot />
  </RadixDropdownMenuCheckboxItem>
</template>
