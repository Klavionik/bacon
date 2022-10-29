import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      name: "login",
      path: "/login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      name: "treats",
      path: "/treats",
      component: () => import("@/views/TreatsView.vue"),
    },
    {
      name: "profile",
      path: "/profile",
      component: () => import("@/views/ProfileView.vue"),
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
