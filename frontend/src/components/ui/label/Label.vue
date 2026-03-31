<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

interface Props {
  for?: string
  class?: string
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  for: '',
  class: '',
  required: false
})

const classes = computed(() => {
  return cn(
    'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
    props.class
  )
})
</script>

<template>
  <label :for="props.for" :class="classes">
    <slot />
    <span v-if="props.required" class="text-red-500 ml-1">*</span>
  </label>
</template>
