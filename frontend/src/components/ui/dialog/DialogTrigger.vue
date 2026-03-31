<script setup lang="ts">
import { DialogTrigger as DialogTriggerRoot } from 'radix-vue'

const props = defineProps<{
  asChild?: boolean
}>()
</script>

<template>
  <DialogTriggerRoot :as-child="asChild">
    <slot />
  </DialogTriggerRoot>
</template>
