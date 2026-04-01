<script setup lang="ts">
import { ref, watch } from "vue"
import { useRoute } from "vue-router"

import AppSidebar from "@/components/shared/AppSidebar.vue"
import AppTopBar from "@/components/shared/AppTopBar.vue"

const route = useRoute()
const mobileOpen = ref(false)

function closeMobileSidebar() {
  mobileOpen.value = false
}

function openMobileSidebar() {
  mobileOpen.value = true
}

function closeSidebarOnNavigation() {
  if (mobileOpen.value) {
    closeMobileSidebar()
  }
}

watch(
  () => route.fullPath,
  () => {
    closeSidebarOnNavigation()
  }
)
</script>

<template>
  <div class="relative min-h-screen overflow-x-hidden bg-background text-foreground">
    <div class="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_15%_15%,hsl(var(--primary)/0.10),transparent_42%),radial-gradient(circle_at_85%_85%,hsl(var(--accent-foreground)/0.06),transparent_46%)]" />

    <AppSidebar
      :mobile-open="mobileOpen"
      @close-mobile="closeMobileSidebar"
    />

    <div class="relative flex min-h-screen flex-1 flex-col md:pl-72">
      <AppTopBar @open-sidebar="openMobileSidebar" />

      <main class="flex-1 p-4 md:p-6">
        <section class="mx-auto flex min-h-[calc(100vh-7rem)] w-full max-w-7xl flex-col rounded-2xl border border-border/80 bg-card/95 p-5 shadow-sm md:p-6">
          <slot />
        </section>
      </main>
    </div>
  </div>
</template>
