<template>
  <div class="w-full">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { provide, ref, watch } from 'vue'

interface Props {
  open?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  open: true
})

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

// 使用内部状态，初始化为传入的值
const internalOpen = ref(props.open)

// 监听外部状态变化
watch(() => props.open, (newValue) => {
  if (internalOpen.value !== newValue) {
    internalOpen.value = newValue
  }
}, { immediate: true })

// 监听内部状态变化，同步到外部
watch(internalOpen, (newValue) => {
  emit('update:open', newValue)
})

const toggle = () => {
  internalOpen.value = !internalOpen.value
}

provide('collapsible', {
  open: internalOpen,
  toggle
})
</script>

<style scoped>
.collapsible {
  width: 100%;
}
</style> 