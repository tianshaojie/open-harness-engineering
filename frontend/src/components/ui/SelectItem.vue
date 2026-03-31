<template>
  <div
    :class="cn('relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-gray-100 focus:bg-gray-100', $attrs.class)"
    @click="handleClick"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  value: string
}>()

const select = inject<{
  updateValue: (value: string) => void
}>('select')

const handleClick = () => {
  select?.updateValue(props.value)
}

defineOptions({
  inheritAttrs: false,
})
</script>
