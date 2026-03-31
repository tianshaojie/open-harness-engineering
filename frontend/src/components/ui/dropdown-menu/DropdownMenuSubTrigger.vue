<script setup lang="ts">
import { DropdownMenuSubTrigger as RadixDropdownMenuSubTrigger } from 'radix-vue'
import { ChevronRight } from 'lucide-vue-next'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
  disabled?: boolean
}>()
</script>

<template>
  <RadixDropdownMenuSubTrigger
    :class="cn(
      'flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent data-[state=open]:bg-accent',
      props.class
    )"
    :disabled="props.disabled"
  >
    <slot />
    <ChevronRight class="ml-auto h-4 w-4" />
  </RadixDropdownMenuSubTrigger>
</template>
