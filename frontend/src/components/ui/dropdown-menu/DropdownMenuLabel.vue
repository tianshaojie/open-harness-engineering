<script setup lang="ts">
import { DropdownMenuLabel as RadixDropdownMenuLabel } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
  inset?: boolean
}>()
</script>

<template>
  <RadixDropdownMenuLabel
    :class="cn(
      'px-2 py-1.5 text-sm font-semibold',
      props.inset && 'pl-8',
      props.class
    )"
  >
    <slot />
  </RadixDropdownMenuLabel>
</template>
