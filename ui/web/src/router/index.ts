import { createRouter, createWebHistory } from "vue-router"
import { authGuard } from "@auth0/auth0-vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      name: "treats",
      path: "/treats",
      component: () => import("@/views/TreatsView.vue"),
      beforeEnter: authGuard,
    },
    {
      name: "profile",
      path: "/profile",
      component: () => import("@/views/ProfileView.vue"),
      beforeEnter: authGuard,
    },
    {
      name: "forbidden",
      path: "/forbidden",
      component: () => import("@/views/ForbiddenView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      component: () => import("@/views/NotFoundView.vue"),
    },
  ],
})

export default router
