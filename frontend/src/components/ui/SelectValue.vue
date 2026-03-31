<template>
  <span>{{ select?.selectedValue.value || placeholder }}</span>
</template>

<script setup lang="ts">
import { inject } from 'vue'

defineProps<{
  placeholder?: string
}>()

const select = inject<{
  selectedValue: { value: string }
}>('select')
</script>
