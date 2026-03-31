<template>
  <section class="rounded-lg border border-border bg-card p-6">
    <h2 class="text-lg font-semibold">Playground Controls</h2>
    <p class="mt-2 text-sm text-slate-600">
      This page is intentionally non-business and exists to validate UI harness, routing, and smoke automation.
    </p>
    <div class="mt-5 flex items-center gap-3">
      <Button @click="counter += 1">Increment</Button>
      <Button variant="outline" @click="counter = 0">Reset</Button>
      <span data-testid="playground-counter" class="rounded-md border border-border px-3 py-2 text-sm font-medium">
        Counter: {{ counter }}
      </span>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue"

import { Button } from "@/components/ui/button"

const counter = ref(0)
</script>
