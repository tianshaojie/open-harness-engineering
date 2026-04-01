<script setup lang="ts">
import SidebarNavGroup from "@/components/shared/SidebarNavGroup.vue"
import { sidebarNavGroups } from "@/components/shared/navigation"

defineProps<{
  mobileOpen: boolean
}>()

const emit = defineEmits<{
  closeMobile: []
}>()

function closeMobile() {
  emit("closeMobile")
}
</script>

<template>
  <aside class="hidden md:fixed md:inset-y-0 md:left-0 md:z-30 md:flex md:w-72 md:flex-col md:border-r md:border-sidebar-border md:bg-sidebar/95 md:backdrop-blur">
    <div class="flex h-16 items-center border-b border-sidebar-border px-6">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">Harness UI</p>
        <p class="text-sm font-semibold">open_harness_engineering</p>
      </div>
    </div>
    <nav class="flex-1 space-y-6 overflow-y-auto px-4 py-5">
      <SidebarNavGroup
        v-for="group in sidebarNavGroups"
        :key="group.title"
        :group="group"
      />
    </nav>
    <footer class="border-t border-sidebar-border px-6 py-4 text-xs text-muted-foreground">
      shadcn-admin inspired foundation shell
    </footer>
  </aside>

  <Transition name="sidebar-fade">
    <div
      v-if="mobileOpen"
      class="fixed inset-0 z-40 bg-slate-950/45 md:hidden"
      @click="closeMobile"
    />
  </Transition>

  <Transition name="sidebar-slide">
    <aside
      v-if="mobileOpen"
      class="fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-sidebar-border bg-sidebar shadow-2xl md:hidden"
    >
      <div class="flex h-16 items-center justify-between border-b border-sidebar-border px-6">
        <p class="text-sm font-semibold">Workspace</p>
        <button
          type="button"
          class="rounded-md px-2 py-1 text-xs font-medium text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          @click="closeMobile"
        >
          Close
        </button>
      </div>
      <nav class="flex-1 space-y-6 overflow-y-auto px-4 py-5">
        <SidebarNavGroup
          v-for="group in sidebarNavGroups"
          :key="`mobile-${group.title}`"
          :group="group"
        />
      </nav>
    </aside>
  </Transition>
</template>

<style scoped>
.sidebar-slide-enter-active,
.sidebar-slide-leave-active {
  transition: transform 180ms ease;
}

.sidebar-slide-enter-from,
.sidebar-slide-leave-to {
  transform: translateX(-100%);
}

.sidebar-fade-enter-active,
.sidebar-fade-leave-active {
  transition: opacity 180ms ease;
}

.sidebar-fade-enter-from,
.sidebar-fade-leave-to {
  opacity: 0;
}
</style>
