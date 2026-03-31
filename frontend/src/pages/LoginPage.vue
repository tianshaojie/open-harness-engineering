<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-md">
      <div>
        <h2 class="text-center text-3xl font-bold text-gray-900">登录</h2>
        <p class="mt-2 text-center text-sm text-gray-600">Open Harness Engineering</p>
      </div>
      
      <div class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">用户名</label>
            <Input
              v-model="username"
              type="text"
              placeholder="请输入用户名"
              class="mt-1"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">密码</label>
            <Input
              v-model="password"
              type="password"
              placeholder="请输入密码"
              class="mt-1"
            />
          </div>
        </div>

        <div v-if="errorMessage" :class="errorMessage.includes('✅') ? 'text-green-600' : 'text-red-600'" class="text-sm text-center p-3 rounded bg-gray-50">
          {{ errorMessage }}
        </div>

        <Button
          type="button"
          :disabled="loading"
          @click.prevent.stop="doLogin"
          class="w-full"
        >
          {{ loading ? '登录中...' : '登录' }}
        </Button>
      </div>

      <div class="text-center text-sm text-gray-500">
        <p>默认账号: superadmin / Admin@123</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Input from '@/components/ui/input/Input.vue'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const doLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    console.log('=== 开始登录 ===')
    console.log('用户名:', username.value)
    console.log('密码:', password.value)
    
    const success = await authStore.login({
      username: username.value,
      password: password.value,
    })

    console.log('登录结果:', success)
    const token = localStorage.getItem('token')
    console.log('Token:', token)

    if (success) {
      errorMessage.value = '✅ 登录成功！Token: ' + (token?.substring(0, 20) || '') + '...'
      console.log('登录成功，3秒后跳转')
      setTimeout(() => {
        console.log('开始跳转')
        router.replace('/')
      }, 3000)
    } else {
      errorMessage.value = '❌ 用户名或密码错误'
      console.log('登录失败')
    }
  } catch (error) {
    errorMessage.value = '❌ 登录失败: ' + String(error)
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>
