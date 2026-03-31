<script setup lang="ts">
import { TabsList as RadixTabsList } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <RadixTabsList
    :class="cn(
      'inline-flex h-auto items-center justify-start rounded-md bg-gray-100 p-1 text-gray-500 w-fit',
      props.class
    )"
  >
    <slot />
  </RadixTabsList>
</template> 