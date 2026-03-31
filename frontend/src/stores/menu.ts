import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sysResourceApi, type SysResource } from '@/api/sys'

export interface MenuItem {
  id: number
  name: string
  path?: string | null
  icon?: string | null
  children?: MenuItem[]
}

export const useMenuStore = defineStore('menu', () => {
  const menuList = ref<SysResource[]>([])
  const loading = ref(false)

  const fetchMenuList = async () => {
    loading.value = true
    try {
      const response = await sysResourceApi.menuList()
      if (response.success && response.data) {
        menuList.value = response.data
      }
    } catch (error) {
      console.error('Failed to fetch menu list:', error)
    } finally {
      loading.value = false
    }
  }

  const menuTree = computed(() => {
    const buildTree = (items: SysResource[], parentId: number): MenuItem[] => {
      return items
        .filter((item) => item.pid === parentId && item.visible === 1)
        .sort((a, b) => a.sort - b.sort)
        .map((item) => ({
          id: item.id,
          name: item.name,
          path: item.path,
          icon: item.icon,
          children: buildTree(items, item.id),
        }))
    }
    return buildTree(menuList.value, 0)
  })

  return {
    menuList,
    menuTree,
    loading,
    fetchMenuList,
  }
})
