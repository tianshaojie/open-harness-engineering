<script setup lang="ts">
import { TabsTrigger as RadixTabsTrigger } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  value: string
  class?: string
  disabled?: boolean
}

const props = defineProps<Props>()
</script>

<template>
  <RadixTabsTrigger
    :value="value"
    :disabled="disabled"
    :class="cn(
      'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-2 py-1 text-xs font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-sm',
      props.class
    )"
  >
    <slot />
  </RadixTabsTrigger>
</template> 