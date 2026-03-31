<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  value: string
  class?: HTMLAttributes['class']
}>()

const emit = defineEmits<{
  select: [value: string]
}>()

const onSelect = () => {
  emit('select', props.value)
}
</script>

<template>
  <div
    :class="cn(
      'relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent hover:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50',
      props.class
    )"
    @click="onSelect"
    v-bind="$attrs"
  >
    <slot />
  </div>
</template>
