<script setup lang="ts">
import { DialogClose as DialogCloseRoot } from 'radix-vue'

const props = defineProps<{
  asChild?: boolean
}>()
</script>

<template>
  <DialogCloseRoot :as-child="asChild">
    <slot />
  </DialogCloseRoot>
</template>
