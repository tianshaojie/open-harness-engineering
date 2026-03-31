<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'
import { cva } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  class?: string
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
}

const props = withDefaults(defineProps<ButtonProps>(), {
  variant: 'default',
  size: 'default',
  class: '',
  type: 'button',
  disabled: false
})

const classes = computed(() => {
  return cn(buttonVariants({ variant: props.variant, size: props.size }), props.class)
})
</script>

<template>
  <button
    :type="type"
    :class="classes"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<style scoped>
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  border: 1px solid transparent;
}

.button--default {
  background-color: #1890ff;
  color: white;
}

.button--default:hover {
  background-color: #40a9ff;
}

.button--ghost {
  background-color: transparent;
  color: #666;
}

.button--ghost:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #1890ff;
}

.button--link {
  background-color: transparent;
  color: #1890ff;
  border: none;
  padding: 0;
}

.button--link:hover {
  color: #40a9ff;
  text-decoration: underline;
}

.button--default {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.button--sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.button--lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}
</style> 