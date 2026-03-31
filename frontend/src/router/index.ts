import { createRouter, createWebHistory } from "vue-router"

import LoginPage from "@/pages/LoginPage.vue"
import MainLayout from "@/layouts/MainLayout.vue"
import HomeOverviewPage from "@/pages/HomeOverviewPage.vue"
import MemberPage from "@/pages/sys/MemberPage.vue"
import OrganizationPage from "@/pages/sys/OrganizationPage.vue"
import RolePage from "@/pages/sys/RolePage.vue"
import NotFoundPage from "@/pages/NotFoundPage.vue"
import PlaygroundPage from "@/pages/PlaygroundPage.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginPage
    },
    {
      path: "/",
      component: MainLayout,
      children: [
        {
          path: "",
          redirect: "/home/overview"
        },
        {
          path: "home/overview",
          name: "home-overview",
          component: HomeOverviewPage
        },
        {
          path: "sys/member",
          name: "sys-member",
          component: MemberPage
        },
        {
          path: "sys/organization",
          name: "sys-organization",
          component: OrganizationPage
        },
        {
          path: "sys/role",
          name: "sys-role",
          component: RolePage
        },
        {
          path: "playground",
          name: "playground",
          component: PlaygroundPage
        }
      ]
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundPage
    }
  ]
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  
  // 白名单路径，不需要登录
  const whiteList = ['/login']
  
  if (whiteList.includes(to.path)) {
    // 如果已登录访问登录页，重定向到首页
    if (token) {
      next('/')
    } else {
      next()
    }
  } else {
    // 其他页面需要登录
    if (token) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router
