import { ref } from 'vue'
import type { VNode } from 'vue'

export type StringOrVNode = string | VNode | (() => VNode)

export type ToasterToast = {
  id: string
  title?: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
  variant?: 'default' | 'destructive' | 'warning' | 'success' | 'error'
  duration?: number
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

const TOAST_LIMIT = 1
const TOAST_REMOVE_DELAY = 1000

const toasts = ref<ToasterToast[]>([])

const toast = ({ ...props }: Omit<ToasterToast, 'id'>) => {
  const id = Math.random().toString(36).substr(2, 9)
  const duration = props.duration || TOAST_REMOVE_DELAY

  toasts.value = [
    {
      ...props,
      id,
      open: true
    }
  ]

  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, duration)
}

export const useToast = () => {
  const dismiss = (toastId?: string) => {
    if (toastId) {
      toasts.value = toasts.value.filter((t) => t.id !== toastId)
    } else {
      toasts.value = []
    }
  }

  return {
    toasts,
    toast,
    dismiss
  }
}

export { toast }
