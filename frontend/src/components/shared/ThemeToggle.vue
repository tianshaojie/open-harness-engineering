<script setup lang="ts">
import { onMounted, ref } from "vue"

import { Button } from "@/components/ui/button"

type ThemeMode = "light" | "dark"

const mode = ref<ThemeMode>("light")

function applyTheme(next: ThemeMode) {
  document.documentElement.classList.toggle("dark", next === "dark")
  window.localStorage.setItem("ohe-theme", next)
}

function toggleTheme() {
  mode.value = mode.value === "light" ? "dark" : "light"
  applyTheme(mode.value)
}

onMounted(() => {
  const stored = window.localStorage.getItem("ohe-theme")
  if (stored === "light" || stored === "dark") {
    mode.value = stored
  } else {
    mode.value = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  }

  applyTheme(mode.value)
})
</script>

<template>
  <Button variant="outline" size="sm" @click="toggleTheme">
    <span v-if="mode === 'light'">Dark</span>
    <span v-else>Light</span>
    <span class="ml-2 text-xs text-muted-foreground">Mode</span>
  </Button>
</template>
