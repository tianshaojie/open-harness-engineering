<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{ class?: HTMLAttributes['class'] }>()
</script>

<template>
  <div class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2">
    <slot />
  </div>
</template>
