import { defineStore } from "pinia"
import type { UserCreate, UserLogin, UserRead } from "@/models/user"
import auth from "@/services/auth"
import api from "@/services/api"
import bot from "@/services/bot"
import storage from "@/services/storage"

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      user: {} as UserRead,
      loggedIn: false,
    }
  },
  actions: {
    async signup(user: UserCreate) {
      await auth.signup(user)
      await this.login(user)
    },
    async login(user: UserLogin) {
      const data = await auth.login(user)
      this.loggedIn = true
      const accessToken = data["access_token"]
      auth.setToken(accessToken)
      api.setToken(accessToken)
      bot.setToken(accessToken)
      storage.setItem("accessToken", accessToken)
      this.user = await auth.getMe()
    },
    async loginByToken(token: string) {
      this.user = await auth.getMe()
      this.loggedIn = true
      auth.setToken(token)
      api.setToken(token)
      bot.setToken(token)
    },
    async logout() {
      auth.setToken("")
      api.setToken("")
      bot.setToken("")
      this.user = {} as UserRead
      this.loggedIn = false
      storage.removeItem("accessToken")
    },
  },
})
