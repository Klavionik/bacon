import { useUserStore, TokenExpired, NoAccessToken } from "@/stores/user"
import type { RouteLocationNormalized } from "vue-router"
import { RouteName } from "@/router/enums"
import { type ProgressFinisher, useProgress } from "@marcoschulte/vue3-progress"
import { useToast } from "vue-toastification"

const progresses = [] as ProgressFinisher[]
const toast = useToast()

export const checkTokenAlive = (to: RouteLocationNormalized) => {
  const { loggedIn, isTokenExpired, logout } = useUserStore()

  if (loggedIn && isTokenExpired()) {
    logout()
    toast.warning("Время сессии истекло. Войдите заново.")
    return { name: RouteName.LOGIN, query: { next: to.fullPath } }
  }
}

export const redirectToProducts = () => {
  const { loggedIn } = useUserStore()

  if (loggedIn) return { name: RouteName.PRODUCTS }
}

export const authenticate = async (to: RouteLocationNormalized) => {
  const { loggedIn, restoreSession } = useUserStore()
  if (loggedIn) return

  try {
    await restoreSession()
  } catch (e) {
    if (e instanceof TokenExpired) {
      toast.warning("Время сессии истекло. Войдите заново.")
      return { name: RouteName.LOGIN, query: { next: to.fullPath } }
    }

    if (e instanceof NoAccessToken) {
      if (to.meta.requiresAuth) {
        return { name: RouteName.LOGIN, query: { next: to.fullPath } }
      }
      return
    }

    throw e
  }
}

export const startProgress = () => {
  progresses.push(useProgress().start())
}

export const finishProgress = () => {
  progresses.forEach((progress) => progress.finish())
}
