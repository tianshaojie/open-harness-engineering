<script setup lang="ts">
import { type HTMLAttributes, computed } from 'vue'
import { cn } from '@/lib/utils'

export interface BadgeProps {
  variant?: 'default' | 'secondary' | 'success' | 'destructive' | 'outline'
  class?: HTMLAttributes['class']
}

const props = withDefaults(defineProps<BadgeProps>(), {
  variant: 'default',
})

const badgeVariants = computed(() => {
  const variants = {
    default: 'border-transparent bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'border-transparent bg-gray-100 text-gray-700 hover:bg-gray-200',
    success: 'border-transparent bg-green-500 text-white hover:bg-green-600',
    destructive: 'border-transparent bg-red-500 text-white hover:bg-red-600',
    outline: 'text-gray-700 border-gray-300 hover:bg-gray-50',
  }
  return variants[props.variant]
})
</script>

<template>
  <div
    :class="cn(
      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
      badgeVariants,
      props.class,
    )"
  >
    <slot />
  </div>
</template>
