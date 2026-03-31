<template>
  <div class="min-h-screen bg-background text-foreground">
    <div class="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-6 md:px-8">
      <AppHeader />
      <main class="mt-6 flex-1 rounded-xl border border-border bg-card p-6 shadow-sm">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from "@/components/shared/AppHeader.vue"
</script>
