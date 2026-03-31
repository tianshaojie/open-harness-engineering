<template>
  <p class="shadcn-card-description">
    <slot />
  </p>
</template>

<style scoped>
.shadcn-card-description {
  color: var(--muted-foreground, #6c7280);
  font-size: 0.875rem;
  line-height: 1.25rem;
  margin: 0;
  margin-top: 0.25rem;
}
</style>
