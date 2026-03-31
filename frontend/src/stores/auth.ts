import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sysLoginApi, type SysLoginRequest, type SysLoginData } from '@/api/sys'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<SysLoginData | null>(null)

  const login = async (credentials: SysLoginRequest) => {
    try {
      const response = await sysLoginApi.login(credentials)
      if (response.success && response.data) {
        // 先保存到localStorage
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('userInfo', JSON.stringify(response.data))
        // 再更新store
        token.value = response.data.token
        userInfo.value = response.data
        return true
      }
      return false
    } catch (error) {
      console.error('Login API error:', error)
      return false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  const initAuth = () => {
    const savedUserInfo = localStorage.getItem('userInfo')
    if (savedUserInfo && token.value) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
      } catch {
        logout()
      }
    }
  }

  return {
    token,
    userInfo,
    login,
    logout,
    initAuth,
  }
})
