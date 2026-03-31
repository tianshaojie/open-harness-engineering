<template>
  <button
    type="button"
    :class="cn('flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50', $attrs.class)"
    @click="select?.toggleOpen()"
  >
    <slot />
    <svg class="h-4 w-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { cn } from '@/lib/utils'

const select = inject<{
  isOpen: { value: boolean }
  toggleOpen: () => void
}>('select')

defineOptions({
  inheritAttrs: false,
})
</script>
