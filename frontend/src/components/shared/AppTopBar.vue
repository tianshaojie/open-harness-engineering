<script setup lang="ts">
import { computed } from "vue"
import { RouterLink, useRoute } from "vue-router"

import ThemeToggle from "@/components/shared/ThemeToggle.vue"
import { topNavItems, type ShellNavItem } from "@/components/shared/navigation"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const emit = defineEmits<{
  openSidebar: []
}>()

const route = useRoute()

const routeTitle = computed(() => {
  const title = route.meta.title
  if (typeof title === "string" && title.length > 0) {
    return title
  }

  return "Workspace"
})

function isActive(item: ShellNavItem) {
  if (item.to === "/") {
    return route.path === "/"
  }

  return route.path === item.to || route.path.startsWith(`${item.to}/`)
}

function openSidebar() {
  emit("openSidebar")
}
</script>

<template>
  <header class="sticky top-0 z-20 border-b border-border/70 bg-background/80 backdrop-blur">
    <div class="mx-auto flex h-16 w-full max-w-7xl items-center gap-3 px-4 md:px-6">
      <Button
        variant="outline"
        size="icon"
        class="md:hidden"
        @click="openSidebar"
      >
        <span aria-hidden="true" class="text-base leading-none">☰</span>
        <span class="sr-only">Open navigation</span>
      </Button>

      <div class="min-w-0">
        <p class="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">Workspace</p>
        <h1 class="truncate text-sm font-semibold md:text-base">{{ routeTitle }}</h1>
      </div>

      <nav class="ml-5 hidden items-center gap-1 lg:flex">
        <RouterLink
          v-for="item in topNavItems"
          :key="item.to"
          :to="item.to"
          :class="cn(
            'rounded-md px-3 py-2 text-sm font-medium transition-colors',
            isActive(item)
              ? 'bg-accent text-accent-foreground'
              : 'text-muted-foreground hover:bg-accent/70 hover:text-foreground'
          )"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="ml-auto flex items-center gap-2">
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>
