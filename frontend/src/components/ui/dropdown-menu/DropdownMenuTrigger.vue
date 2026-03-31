<script setup lang="ts">
import { DropdownMenuTrigger as RadixDropdownMenuTrigger } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  class?: string
  disabled?: boolean
}

const props = defineProps<Props>()
</script>

<template>
  <RadixDropdownMenuTrigger
    :class="cn(
      'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
      props.class
    )"
    :disabled="props.disabled"
  >
    <slot />
  </RadixDropdownMenuTrigger>
</template>
