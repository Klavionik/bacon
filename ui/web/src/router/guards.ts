import { useUserStore } from "@/stores/user"
import type { RouteLocationNormalized } from "vue-router"
import { RouteName } from "@/router/enums"
import { type ProgressFinisher, useProgress } from "@marcoschulte/vue3-progress"
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
  const userStore = useUserStore()
  if (userStore.loggedIn) return

  const success = await userStore.restoreSession()

  if (!success && to.meta.requiresAuth) {
    toast.warning("Время сессии истекло. Войдите заново.")
    return { name: RouteName.LOGIN, query: { next: to.fullPath } }
  }
}

export const startProgress = () => {
  progresses.push(useProgress().start())
}

export const finishProgress = () => {
  progresses.forEach((progress) => progress.finish())
}
