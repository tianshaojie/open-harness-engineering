<script setup lang="ts">
import { SelectValue as SelectValuePrimitive } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
  placeholder?: string
}>()
</script>

<template>
  <SelectValuePrimitive
    :class="cn('placeholder:text-muted-foreground', props.class)"
    :placeholder="placeholder"
  >
    <slot />
  </SelectValuePrimitive>
</template>
