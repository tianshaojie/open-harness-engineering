<script setup lang="ts">
import { SelectRoot } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
  modelValue?: string | number
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
}>()
</script>

<template>
  <SelectRoot
    :class="cn('relative', props.class)"
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <slot />
  </SelectRoot>
</template>
