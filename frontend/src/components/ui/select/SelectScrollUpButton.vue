<script setup lang="ts">
import { SelectScrollUpButton } from 'radix-vue'
import { cn } from '@/lib/utils'
import { ChevronUp } from 'lucide-vue-next'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <SelectScrollUpButton
    :class="cn('flex cursor-default items-center justify-center py-1', props.class)"
  >
    <slot>
      <ChevronUp class="h-4 w-4" />
    </slot>
  </SelectScrollUpButton>
</template>
