<template>
  <section class="flex min-h-[280px] flex-col items-start justify-center gap-4">
    <p class="text-xs uppercase tracking-[0.16em] text-muted-foreground">404</p>
    <h2 class="text-2xl font-semibold">Page Not Found</h2>
    <p class="max-w-lg text-sm text-muted-foreground md:text-base">
      The route does not exist in this scaffold. Use the sidebar or return to the overview page.
    </p>
    <RouterLink to="/">
      <Button size="sm">Back To Overview</Button>
    </RouterLink>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router"

import { Button } from "@/components/ui/button"
</script>
