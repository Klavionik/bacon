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
      path: "/settings",
      component: () => import("@/views/SettingsView.vue"),
      children: [
        {
          name: "profile",
          path: "profile",
          component: () => import("@/components/UserProfile.vue"),
        },
        {
          name: "shops",
          path: "shops",
          component: () => import("@/components/UserShops.vue"),
        },
        {
          name: "notifications",
          path: "notifications",
          component: () => import("@/components/UserNotifications.vue"),
        },
      ],
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
