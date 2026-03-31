<script setup lang="ts">
import { Command as CommandPrimitive } from 'cmdk-sv'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <CommandPrimitive
    :class="cn(
      'flex h-full w-full flex-col overflow-hidden rounded-md bg-popover text-popover-foreground',
      props.class
    )"
  >
    <slot />
  </CommandPrimitive>
</template>
