import { defineStore } from "pinia"
import type { UserCreate, UserLogin, UserRead } from "@/models/user"
import auth from "@/services/auth"
import api from "@/services/api"
import bot from "@/services/bot"
import storage from "@/services/storage"
import { BadRequest } from "@/services/http"
import { useToast } from "vue-toastification"

const BAD_CREDENTIALS = "LOGIN_BAD_CREDENTIALS"

const toast = useToast()

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      user: {} as UserRead,
      loggedIn: false,
    }
  },
  actions: {
    async onLogin(data: any) {
      this.loggedIn = true
      const accessToken = data["access_token"]
      auth.setToken(accessToken)
      api.setToken(accessToken)
      bot.setToken(accessToken)
      storage.setItem("accessToken", accessToken)
      this.user = await auth.getMe()
    },
    async signup(user: UserCreate) {
      await auth.signup(user)
      await this.login(user)
    },
    async login(user: UserLogin) {
      try {
        const data = await auth.login(user)
        await this.onLogin(data)
      } catch (e) {
        if (!(e instanceof BadRequest)) throw e

        if (e.detail === BAD_CREDENTIALS) {
          toast.warning("Неправильный пароль и/или email.")
        }
      }
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
