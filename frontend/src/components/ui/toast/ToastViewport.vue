<script setup lang="ts">
import { ToastViewport as ToastViewportRoot } from 'radix-vue'
import { cn } from '@/lib/utils'
</script>

<template>
  <ToastViewportRoot
    class="fixed top-0 left-1/2 -translate-x-1/2 flex max-h-screen flex-col-reverse p-4 z-[9999]"
  >
    <slot />
  </ToastViewportRoot>
</template>
