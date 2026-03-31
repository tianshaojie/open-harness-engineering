<template>
  <nav :class="['shadcn-navigation-menu', props.class]">
    <ul class="shadcn-navigation-menu-list">
      <slot />
    </ul>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{ class?: string }>()
</script>

<style scoped>
.shadcn-navigation-menu {
  width: 100%;
  background: transparent;
  padding: 0;
}
.shadcn-navigation-menu-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style> 