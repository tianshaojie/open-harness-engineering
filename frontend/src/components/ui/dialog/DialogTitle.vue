<script setup lang="ts">
import { DialogTitle as DialogTitleRoot } from 'radix-vue'
</script>

<template>
  <DialogTitleRoot class="text-lg font-semibold leading-none tracking-tight">
    <slot />
  </DialogTitleRoot>
</template>
