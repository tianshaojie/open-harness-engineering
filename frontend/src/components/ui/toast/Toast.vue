<script setup lang="ts">
import { ToastRoot } from 'radix-vue'
import type { HTMLAttributes, VNode } from 'vue'
import { cn } from '@/lib/utils'
import { CheckCircle2, AlertCircle, XCircle, Info } from 'lucide-vue-next'

type StringOrVNode = string | VNode | (() => VNode)

const props = defineProps<{
  variant?: 'default' | 'destructive' | 'warning' | 'success' | 'error'
  class?: HTMLAttributes['class']
  id?: string
  title?: StringOrVNode
}>()

const getIcon = () => {
  switch (props.variant) {
    case 'success':
      return CheckCircle2
    case 'warning':
      return AlertCircle
    case 'error':
    case 'destructive':
      return XCircle
    default:
      return Info
  }
}

const Icon = getIcon()
</script>

<template>
  <ToastRoot
    :class="
      cn(
        'group pointer-events-auto relative flex items-start gap-3 rounded-lg px-4 py-3 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-all duration-300 ease-in-out data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-top-full data-[state=open]:slide-in-from-top-full min-w-[200px] max-w-[600px]',
        {
          'bg-white text-gray-900': props.variant === 'default',
          'bg-red-500 text-white': ['destructive', 'error'].includes(props.variant || ''),
          'bg-yellow-500 text-white': props.variant === 'warning',
          'bg-green-500 text-white': props.variant === 'success'
        },
        props.class,
      )"
  >
    <Icon class="h-4 w-4 flex-shrink-0 mt-0.5" />
    <div class="text-sm leading-6 break-words">
      <slot />
    </div>
  </ToastRoot>
</template>

<style>
@keyframes slide-in-from-top {
  from {
    opacity: 0;
    transform: translateY(-100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-out-to-top {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-100%);
  }
}

/* PC端样式 */
@media (min-width: 769px) {
  .ToastRoot, .toast, .ant-toast, .group.pointer-events-auto {
    font-size: 14px !important;
    max-width: 600px !important;
    min-width: 200px !important;
  }
  
  .ToastRoot div, .toast div, .ant-toast div, .group.pointer-events-auto div {
    line-height: 1.5 !important;
    word-break: break-word !important;
    white-space: normal !important;
  }
}

@media (max-width: 768px) {
  .ToastRoot, .toast, .ant-toast, .group.pointer-events-auto {
    font-size: 13px !important;
    max-width: calc(100vw - 32px) !important;
    min-width: 200px !important;
  }
  
  .ToastRoot div, .toast div, .ant-toast div, .group.pointer-events-auto div {
    line-height: 1.43 !important;
    word-break: break-word !important;
    white-space: normal !important;
  }
}
</style>
