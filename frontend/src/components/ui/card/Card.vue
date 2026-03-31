<template>
  <div :class="['shadcn-card', props.class]">
    <div v-if="$slots.header" class="shadcn-card-header">
      <slot name="header" />
    </div>
    <div class="shadcn-card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="shadcn-card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ class?: string }>()
</script>

<style scoped>
.shadcn-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px 0 rgba(16, 30, 54, 0.04);
  border: 1px solid #f0f0f0;
  padding: 24px;
  transition: box-shadow 0.2s;
}
.shadcn-card-header {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}
.shadcn-card-body {
  font-size: 15px;
}
.shadcn-card-footer {
  margin-top: 16px;
  text-align: right;
}
</style> 