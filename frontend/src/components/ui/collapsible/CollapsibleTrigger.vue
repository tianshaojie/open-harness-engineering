<template>
  <button
    type="button"
    class="w-full flex items-center justify-between px-5 py-3 text-sm font-medium text-gray-700 bg-white rounded-lg transition-all hover:text-primary hover:bg-gray-50 border border-gray-200"
    @click="toggle"
  >
    <slot />
    <ChevronDown 
      class="h-4 w-4 transition-transform duration-200" 
      :class="{ 'rotate-180': open }" 
    />
  </button>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const { open, toggle } = inject('collapsible', { open: false, toggle: () => {} })
</script>

<style>
.collapsible-trigger {
  all: unset;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  cursor: pointer;
  border: none;
  outline: none;
  transition: all 0.2s;
}

.collapsible-trigger:hover {
  border: none;
  outline: none;
}

.collapsible-trigger:focus {
  border: none;
  outline: none;
  box-shadow: none;
}
</style> 