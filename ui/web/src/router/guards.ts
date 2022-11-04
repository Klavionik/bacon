import { useUserStore } from "@/stores/user"
import type { RouteLocationNormalized } from "vue-router"
import { RouteName } from "@/router/enums"
import storage from "@/services/storage"
import { type ProgressFinisher, useProgress } from "@marcoschulte/vue3-progress"
import { Unauthorized } from "@/services/http"
import auth from "@/services/auth"
import { useToast } from "vue-toastification"

const progresses = [] as ProgressFinisher[]
const toast = useToast()

export const checkLoggedIn = (to: RouteLocationNormalized) => {
  const { loggedIn } = useUserStore()

  if (!loggedIn && to.name !== RouteName.LOGIN) {
    return { name: RouteName.LOGIN }
  }
}

export const authenticate = async (to: RouteLocationNormalized) => {
  const { loggedIn } = useUserStore()
  if (loggedIn) return

  const savedToken = storage.getItem("accessToken")
  if (savedToken === null) return

  const userStore = useUserStore()
  auth.setToken(savedToken)

  try {
    await userStore.loginByToken(savedToken)
  } catch (e: any) {
    if (!(e instanceof Unauthorized)) throw e

    storage.removeItem("accessToken")
    auth.removeToken()

    if (to.meta.requiresAuth) {
      toast.warning("Время сессии истекло. Войдите заново.")
      return { name: RouteName.LOGIN, query: { next: to.fullPath } }
    }
  }
}

export const startProgress = () => {
  progresses.push(useProgress().start())
}

export const finishProgress = () => {
  progresses.forEach((progress) => progress.finish())
}
