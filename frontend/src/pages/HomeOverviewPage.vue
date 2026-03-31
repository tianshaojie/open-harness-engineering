<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">概览</h1>
      <p class="mt-1 text-sm text-gray-500">系统概览和统计信息</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">总用户数</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">-</p>
          </div>
          <div class="p-3 bg-blue-100 rounded-lg">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">总角色数</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">-</p>
          </div>
          <div class="p-3 bg-green-100 rounded-lg">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">总资源数</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">-</p>
          </div>
          <div class="p-3 bg-purple-100 rounded-lg">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg border border-gray-200">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">欢迎使用 Open Harness Engineering</h2>
      <p class="text-gray-600">
        这是一个AI-native全栈脚手架，集成了完整的RBAC权限管理系统。
      </p>
      <div class="mt-4 space-y-2">
        <p class="text-sm text-gray-600">• 用户管理：管理系统用户和组织架构</p>
        <p class="text-sm text-gray-600">• 角色管理：配置角色和权限</p>
        <p class="text-sm text-gray-600">• 资源管理：管理菜单和功能权限</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 概览页面
</script>
