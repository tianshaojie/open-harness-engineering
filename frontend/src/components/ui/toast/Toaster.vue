<script setup lang="ts">
import { Toast, ToastViewport } from '@/components/ui/toast'
import { useToast } from './use-toast'

const { toasts } = useToast()
</script>

<template>
  <ToastViewport>
    <Toast 
      v-for="toast in toasts" 
      :key="toast.id" 
      :variant="toast.variant || 'default'"
      :id="toast.id"
    >
      <div v-if="toast.title" class="text-sm font-semibold leading-none">
        {{ toast.title }}
      </div>
    </Toast>
  </ToastViewport>
</template>
