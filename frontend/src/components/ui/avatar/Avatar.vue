<template>
  <div :class="['shadcn-avatar', props.class]">
    <img v-if="src" :src="src" :alt="alt" class="shadcn-avatar-img" @error="onError" />
    <div v-else class="shadcn-avatar-fallback">
      <slot>{{ fallbackText }}</slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{
  src?: string
  alt?: string
  fallbackText?: string
  class?: string
}>()
const errored = ref(false)
const onError = () => {
  errored.value = true
}
</script>

<style scoped>
.shadcn-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #64748b;
}
.shadcn-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.shadcn-avatar-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  color: #64748b;
}
</style> 