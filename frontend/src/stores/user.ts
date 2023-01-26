import { defineStore } from "pinia"
import type { UserCreate, UserLogin, UserRead } from "@/models/user"
import { services, client } from "@/http/"
import storage from "@/storage"
import { BadRequest, Unauthorized } from "@/http/errors"
import { useToast } from "vue-toastification"

const BAD_CREDENTIALS = "LOGIN_BAD_CREDENTIALS"
const DUPLICATE_USER = "REGISTER_USER_ALREADY_EXISTS"

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
      client.setToken(accessToken)
      storage.setItem("accessToken", accessToken)
      this.user = await services.getMe()
    },
    async signup(user: UserCreate) {
      try {
        await services.signup(user)
        await this.login(user)
      } catch (e) {
        if (!(e instanceof BadRequest)) throw e

        if (e.detail === DUPLICATE_USER) {
          toast.warning("Пользователь с таким email уже существует.")
        }
      }
    },
    async login(user: UserLogin) {
      try {
        const data = await services.login(user)
        await this.onLogin(data)
      } catch (e) {
        if (!(e instanceof BadRequest)) throw e

        if (e.detail === BAD_CREDENTIALS) {
          toast.warning("Неправильный пароль и/или email.")
        }
      }
    },
    async loginByToken(token: string) {
      this.user = await services.getMe()
      this.loggedIn = true
      client.setToken(token)
    },
    async logout() {
      client.removeToken()
      this.user = {} as UserRead
      this.loggedIn = false
      storage.removeItem("accessToken")
    },
    async restoreSession() {
      const savedToken = storage.getItem("accessToken")
      if (savedToken === null) return false

      client.setToken(savedToken)

      try {
        await this.loginByToken(savedToken)
        return true
      } catch (e: any) {
        if (!(e instanceof Unauthorized)) throw e

        storage.removeItem("accessToken")
        client.removeToken()
        return false
      }
    },
  },
})
