<template>
  <section class="space-y-6">
    <div class="space-y-2">
      <p class="text-xs uppercase tracking-[0.16em] text-muted-foreground">Foundation Dashboard</p>
      <h2 class="text-2xl font-semibold">AI-native scaffold workspace</h2>
      <p class="max-w-3xl text-sm text-muted-foreground md:text-base">
        This shell is adapted from the shadcn-admin layout style and reserved for harness-level verification.
        Keep backend and frontend implementation non-business, observable, and easy for AI agents to navigate.
      </p>
    </div>

    <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      <article class="rounded-xl border border-border bg-background/80 p-4">
        <p class="text-xs uppercase tracking-[0.14em] text-muted-foreground">Planning</p>
        <h3 class="mt-2 text-base font-semibold">Execution Plans First</h3>
        <p class="mt-2 text-sm text-muted-foreground">
          Non-trivial work should start from docs/exec-plans and be validated before merge.
        </p>
      </article>

      <article class="rounded-xl border border-border bg-background/80 p-4">
        <p class="text-xs uppercase tracking-[0.14em] text-muted-foreground">Validation</p>
        <h3 class="mt-2 text-base font-semibold">Command Parity</h3>
        <p class="mt-2 text-sm text-muted-foreground">
          Lint, typecheck, tests, and smoke commands in README are expected to run as documented.
        </p>
      </article>

      <article class="rounded-xl border border-border bg-background/80 p-4 md:col-span-2 xl:col-span-1">
        <p class="text-xs uppercase tracking-[0.14em] text-muted-foreground">Smoke Surface</p>
        <h3 class="mt-2 text-base font-semibold">Playground Route</h3>
        <p class="mt-2 text-sm text-muted-foreground">
          Use <RouterLink to="/playground" class="font-medium text-primary underline-offset-4 hover:underline">/playground</RouterLink>
          for UI and E2E baseline checks.
        </p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router"
</script>
