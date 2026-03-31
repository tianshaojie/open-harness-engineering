<script setup lang="ts">
import { DropdownMenuRadioGroup as RadixDropdownMenuRadioGroup } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
  value?: string
  onValueChange?: (value: string) => void
}>()
</script>

<template>
  <RadixDropdownMenuRadioGroup
    :class="cn('', props.class)"
    :value="value"
    :on-value-change="onValueChange"
  >
    <slot />
  </RadixDropdownMenuRadioGroup>
</template>
