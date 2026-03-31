<script setup lang="ts">
import { SelectScrollDownButton } from 'radix-vue'
import { cn } from '@/lib/utils'
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <SelectScrollDownButton
    :class="cn('flex cursor-default items-center justify-center py-1', props.class)"
  >
    <slot>
      <ChevronDown class="h-4 w-4" />
    </slot>
  </SelectScrollDownButton>
</template>
