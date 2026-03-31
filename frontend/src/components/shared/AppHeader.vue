<template>
  <header class="flex flex-col gap-4 rounded-xl border border-border bg-card p-4 md:flex-row md:items-center md:justify-between">
    <div>
      <p class="text-xs uppercase tracking-[0.18em] text-slate-500">Harness Engineering</p>
      <h1 class="text-xl font-semibold">open_harness_engineering</h1>
    </div>
    <nav class="flex items-center gap-2">
      <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100">
        {{ item.label }}
      </RouterLink>
    </nav>
  </header>
</template>

<script setup lang="ts">
const navItems = [
  { to: "/", label: "Home" },
  { to: "/playground", label: "Playground" }
]
</script>
