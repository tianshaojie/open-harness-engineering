<script setup lang="ts">
import { SelectGroup as SelectGroupPrimitive } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <SelectGroupPrimitive
    :class="cn('p-1', props.class)"
  >
    <slot />
  </SelectGroupPrimitive>
</template>
