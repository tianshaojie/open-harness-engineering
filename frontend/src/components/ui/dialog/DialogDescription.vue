<script setup lang="ts">
import { DialogDescription as DialogDescriptionRoot } from 'radix-vue'
</script>

<template>
  <DialogDescriptionRoot class="text-sm text-muted-foreground">
    <slot />
  </DialogDescriptionRoot>
</template>
