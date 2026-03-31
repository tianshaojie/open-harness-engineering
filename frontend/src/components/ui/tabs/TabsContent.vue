<script setup lang="ts">
import { TabsContent as RadixTabsContent } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props {
  value: string
  class?: string
  forceMount?: boolean
}

const props = defineProps<Props>()
</script>

<template>
  <RadixTabsContent
    :value="value"
    :force-mount="props.forceMount"
    :class="cn(
      'mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
      props.class
    )"
  >
    <slot />
  </RadixTabsContent>
</template> 