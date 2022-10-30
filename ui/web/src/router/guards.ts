import { useUserStore } from "@/stores/users"
import type { RouteLocationNormalized } from "vue-router"
import { RouteName } from "@/router/enums"

export const checkLoggedIn = (to: RouteLocationNormalized) => {
  const { loggedIn } = useUserStore()

  if (!loggedIn && to.name !== RouteName.LOGIN) {
    return { name: RouteName.LOGIN }
  }
}

export const authenticate = (to: RouteLocationNormalized) => {}
