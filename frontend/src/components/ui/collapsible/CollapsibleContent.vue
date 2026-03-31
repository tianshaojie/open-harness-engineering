<template>
  <div
    v-show="open"
    class="mt-2"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'

const { open } = inject('collapsible', { open: false })
</script>

<style scoped>
.collapsible-content {
  margin-top: 8px;
}
</style> 