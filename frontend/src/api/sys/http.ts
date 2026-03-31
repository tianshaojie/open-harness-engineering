import axios, { type AxiosRequestConfig } from 'axios'
import router from '@/router'
import { toast } from '@/components/ui/toast/use-toast'

const SYS_TOKEN_KEY = 'sys_token'
const TOKEN_KEY = 'token'

const sysHttp = axios.create({
  baseURL: (() => {
    const protocol = window.location.protocol
    const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
    if (baseUrl.startsWith('http://') || baseUrl.startsWith('https://')) {
      return baseUrl.replace(/^https?:\/\//, `${protocol}//`)
    }
    return baseUrl
  })(),
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

sysHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

sysHttp.interceptors.response.use(
  (response) => {
    const data = response.data
    return data
  },
  (error) => {
    if (error.response?.status === 401) {
      // 如果是用普通token访问的，跳回主登录页
      const hasMainToken = !!localStorage.getItem(TOKEN_KEY)
      if (hasMainToken) {
        localStorage.removeItem(TOKEN_KEY)
        router.replace('/login')
      } else {
        localStorage.removeItem(SYS_TOKEN_KEY)
        router.replace('/sys/login')
      }
    } else {
      const msg = error.response?.data?.message || '请求失败'
      toast({ variant: 'destructive', title: msg })
    }
    return Promise.reject(error)
  }
)

export async function sysPost<T = any>(url: string, data?: any): Promise<T> {
  const res = await sysHttp.post(url, data)
  return res as unknown as T
}
