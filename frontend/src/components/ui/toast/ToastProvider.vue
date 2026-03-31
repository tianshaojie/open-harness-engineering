<script setup lang="ts">
import { ToastProvider as ToastProviderRoot } from 'radix-vue'
</script>

<template>
  <ToastProviderRoot>
    <slot />
  </ToastProviderRoot>
</template>
