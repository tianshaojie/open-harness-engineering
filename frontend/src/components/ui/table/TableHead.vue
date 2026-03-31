<script setup lang="ts">
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <th :class="cn('px-4 text-left align-middle font-medium text-black bg-transparent [&:has([role=checkbox])]:pr-0', props.class)">
    <slot />
  </th>
</template> 