<script setup lang="ts">
import { TabsRoot } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  defaultValue?: string
  modelValue?: string
  orientation?: 'horizontal' | 'vertical'
  dir?: 'ltr' | 'rtl'
  activationMode?: 'automatic' | 'manual'
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  orientation: 'horizontal',
  activationMode: 'automatic'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <TabsRoot
    :class="cn('', props.class)"
    :default-value="defaultValue"
    :model-value="modelValue"
    :orientation="orientation"
    :dir="dir"
    :activation-mode="activationMode"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <slot />
  </TabsRoot>
</template> 