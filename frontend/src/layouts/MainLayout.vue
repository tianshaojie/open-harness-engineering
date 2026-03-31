<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900">
              Open Harness Engineering
            </h1>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-sm text-gray-600">
              {{ authStore.userInfo?.real_name || authStore.userInfo?.username }}
            </span>
            <Button variant="outline" size="sm" @click="handleLogout">
              退出登录
            </Button>
          </div>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- 侧边栏菜单 -->
      <aside class="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-4rem)]">
        <nav class="p-4 space-y-1">
          <template v-for="menu in menuStore.menuTree" :key="menu.id">
            <!-- 一级菜单（目录） -->
            <div v-if="menu.children && menu.children.length > 0" class="mb-4">
              <div class="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                {{ menu.name }}
              </div>
              <!-- 二级菜单 -->
              <router-link
                v-for="child in menu.children"
                :key="child.id"
                :to="child.path || '/'"
                class="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md transition-colors"
                :class="isActive(child.path) 
                  ? 'bg-gray-100 text-gray-900' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
              >
                <component :is="getIcon(child.icon)" v-if="child.icon" class="w-5 h-5" />
                <span>{{ child.name }}</span>
              </router-link>
            </div>
            <!-- 单独的菜单项 -->
            <router-link
              v-else
              :to="menu.path || '/'"
              class="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md transition-colors"
              :class="isActive(menu.path) 
                ? 'bg-gray-100 text-gray-900' 
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
            >
              <component :is="getIcon(menu.icon)" v-if="menu.icon" class="w-5 h-5" />
              <span>{{ menu.name }}</span>
            </router-link>
          </template>
        </nav>
      </aside>

      <!-- 主内容区 -->
      <main class="flex-1 p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Home, Settings, Building2, ShieldCheck, Lock } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth'
import { useMenuStore } from '@/stores/menu'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const menuStore = useMenuStore()

const iconMap: Record<string, unknown> = {
  Home,
  Settings,
  Building2,
  ShieldCheck,
  Lock,
}

const getIcon = (iconName?: string) => {
  if (!iconName) return null
  return iconMap[iconName] || Home
}

const isActive = (path?: string) => {
  if (!path) return false
  return route.path === path || route.path.startsWith(path + '/')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  menuStore.fetchMenuList()
})
</script>
