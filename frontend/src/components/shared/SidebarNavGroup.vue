<script setup lang="ts">
import { computed } from "vue"
import { RouterLink, useRoute } from "vue-router"

import type { ShellNavGroup, ShellNavItem } from "@/components/shared/navigation"
import { cn } from "@/lib/utils"

const props = defineProps<{
  group: ShellNavGroup
}>()

const route = useRoute()

const groupItems = computed(() => props.group.items)

function isItemActive(item: ShellNavItem) {
  if (item.disabled) {
    return false
  }

  if (item.to === "/") {
    return route.path === "/"
  }

  return route.path === item.to || route.path.startsWith(`${item.to}/`)
}

const itemClass =
  "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors"
</script>

<template>
  <section class="space-y-2">
    <p class="px-3 text-xs uppercase tracking-[0.16em] text-muted-foreground">
      {{ group.title }}
    </p>
    <ul class="space-y-1">
      <li v-for="item in groupItems" :key="`${group.title}-${item.label}`">
        <span
          v-if="item.disabled"
          :class="cn(itemClass, 'cursor-not-allowed bg-transparent text-muted-foreground/70')"
        >
          <span>{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="rounded-full border border-border px-2 py-0.5 text-[10px] uppercase tracking-[0.12em]"
          >
            {{ item.badge }}
          </span>
        </span>
        <RouterLink
          v-else
          :to="item.to"
          :class="cn(
            itemClass,
            isItemActive(item)
              ? 'bg-sidebar-accent text-sidebar-accent-foreground'
              : 'text-muted-foreground hover:bg-sidebar-accent/60 hover:text-foreground'
          )"
        >
          <span>{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="rounded-full border border-sidebar-border px-2 py-0.5 text-[10px] uppercase tracking-[0.12em]"
          >
            {{ item.badge }}
          </span>
        </RouterLink>
      </li>
    </ul>
  </section>
</template>
