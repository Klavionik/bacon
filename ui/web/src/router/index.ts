import { createRouter, createWebHistory } from "vue-router"
import { checkLoggedIn } from "@/router/guards"
import { RouteName } from "@/router/enums"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: RouteName.HOME,
      path: "/",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      name: RouteName.LOGIN,
      path: "/login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      name: RouteName.TREATS,
      path: "/treats",
      component: () => import("@/views/TreatsView.vue"),
      beforeEnter: checkLoggedIn,
    },
    {
      path: "/settings",
      component: () => import("@/views/SettingsView.vue"),
      beforeEnter: checkLoggedIn,
      children: [
        {
          name: RouteName.SETTINGS_PROFILE,
          path: "profile",
          component: () => import("@/components/UserProfile.vue"),
        },
        {
          name: RouteName.SETTINGS_SHOPS,
          path: "shops",
          component: () => import("@/components/UserShops.vue"),
        },
        {
          name: RouteName.SETTINGS_NOTIFICATIONS,
          path: "notifications",
          component: () => import("@/components/UserNotifications.vue"),
        },
      ],
    },
    {
      name: RouteName.FORBIDDEN,
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
