<template>
  <section class="space-y-6">
    <div class="space-y-2">
      <h2 class="text-2xl font-semibold">Playground</h2>
      <p class="text-slate-700">
        Route dedicated to smoke testing and UI harness verification.
      </p>
    </div>
    <PlaygroundCard />
  </section>
</template>

<script setup lang="ts">
import PlaygroundCard from "@/components/playground/PlaygroundCard.vue"
</script>
