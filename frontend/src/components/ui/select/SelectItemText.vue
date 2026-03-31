<script setup lang="ts">
import { SelectItemText } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <SelectItemText :class="cn(props.class)">
    <slot />
  </SelectItemText>
</template>
