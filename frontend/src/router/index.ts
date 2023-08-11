import { createRouter, createWebHistory } from "vue-router"
import {
  redirectToProducts,
  authenticate,
  startProgress,
  finishProgress,
  checkTokenAlive,
} from "@/router/guards"
import { RouteName } from "@/router/enums"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: () => import("@/views/AppView.vue"),
      children: [
        {
          name: RouteName.HOME,
          path: "",
          component: () => import("@/views/HomeView.vue"),
        },
        {
          name: RouteName.LOGIN,
          path: "login",
          beforeEnter: redirectToProducts,
          component: () => import("@/views/LoginView.vue"),
        },
        {
          name: RouteName.PRODUCTS,
          path: "products",
          component: () => import("@/views/ProductsView.vue"),
          meta: {
            requiresAuth: true,
          },
        },
        {
          path: "settings",
          component: () => import("@/views/SettingsView.vue"),
          meta: {
            requiresAuth: true,
          },
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

router.beforeEach(startProgress)
router.beforeEach(authenticate)
router.beforeEach(checkTokenAlive)

router.afterEach(finishProgress)

export default router
