import { createRouter, createWebHistory } from "vue-router"

import HomePage from "@/pages/HomePage.vue"
import NotFoundPage from "@/pages/NotFoundPage.vue"
import PlaygroundPage from "@/pages/PlaygroundPage.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
      meta: {
        title: "Overview"
      }
    },
    {
      path: "/playground",
      name: "playground",
      component: PlaygroundPage,
      meta: {
        title: "Playground"
      }
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundPage,
      meta: {
        title: "Not Found"
      }
    }
  ]
})

export default router
