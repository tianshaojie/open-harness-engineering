<template>
  <div class="relative">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { provide, ref } from 'vue'

const props = defineProps<{
  modelValue?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const isOpen = ref(false)
const selectedValue = ref(props.modelValue || '')

const updateValue = (value: string) => {
  selectedValue.value = value
  emit('update:modelValue', value)
  isOpen.value = false
}

provide('select', {
  isOpen,
  selectedValue,
  updateValue,
  toggleOpen: () => {
    isOpen.value = !isOpen.value
  },
})
</script>
