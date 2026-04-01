<template>
  <section class="space-y-6">
    <div class="space-y-2">
      <p class="text-xs uppercase tracking-[0.16em] text-muted-foreground">Smoke Workspace</p>
      <h2 class="text-2xl font-semibold">Playground Lab</h2>
      <p class="max-w-2xl text-sm text-muted-foreground md:text-base">
        This route stays intentionally lightweight and non-business. It is the default target for interaction
        smoke tests and quick UI experiments.
      </p>
    </div>

    <PlaygroundCard />
  </section>
</template>

<script setup lang="ts">
import PlaygroundCard from "@/components/playground/PlaygroundCard.vue"
</script>
