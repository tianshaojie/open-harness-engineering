<template>
  <div
    v-if="select?.isOpen.value"
    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border border-gray-200 bg-white py-1 shadow-lg"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'

const select = inject<{
  isOpen: { value: boolean }
}>('select')
</script>
