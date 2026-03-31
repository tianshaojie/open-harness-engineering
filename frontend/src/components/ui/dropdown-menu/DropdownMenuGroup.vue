<script setup lang="ts">
import { DropdownMenuGroup as RadixDropdownMenuGroup } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <RadixDropdownMenuGroup
    :class="cn('p-1', props.class)"
  >
    <slot />
  </RadixDropdownMenuGroup>
</template>
