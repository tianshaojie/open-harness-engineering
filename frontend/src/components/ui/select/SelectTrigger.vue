<script setup lang="ts">
import { SelectTrigger, SelectIcon } from 'radix-vue'
import { cn } from '@/lib/utils'
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <SelectTrigger
    :class="cn(
      'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none disabled:cursor-not-allowed disabled:opacity-50',
      props.class
    )"
  >
    <slot />
    <SelectIcon as-child>
      <ChevronDown class="h-4 w-4 opacity-50" />
    </SelectIcon>
  </SelectTrigger>
</template>
