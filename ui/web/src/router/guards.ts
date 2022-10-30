import { useUserStore } from "@/stores/users"
import type { RouteLocationNormalized } from "vue-router"
import { RouteName } from "@/router/enums"
import storage from "@/services/storage"
import { type ProgressFinisher, useProgress } from "@marcoschulte/vue3-progress"

const progresses = [] as ProgressFinisher[]

export const checkLoggedIn = (to: RouteLocationNormalized) => {
  const { loggedIn } = useUserStore()

  if (!loggedIn && to.name !== RouteName.LOGIN) {
    return { name: RouteName.LOGIN }
  }
}

export const authenticate = async () => {
  const { loggedIn } = useUserStore()
  if (loggedIn) return

  const savedToken = storage.getItem("accessToken")
  if (savedToken === null) return

  const userStore = useUserStore()
  await userStore.loginByToken(savedToken)
}

export const startProgress = () => {
  progresses.push(useProgress().start())
}

export const finishProgress = () => {
  progresses.pop()?.finish()
}
