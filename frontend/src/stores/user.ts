import { defineStore } from "pinia"
import type { UserCreate, UserCreateServer, UserLogin, UserRead } from "@/models/user"
import { services, client } from "@/http/"
import storage from "@/storage"
import { BadRequest, TokenExpired, Unauthorized } from "@/http/errors"
import { useToast } from "vue-toastification"

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
      const accessToken = data["access"]
      client.setToken(accessToken)
      storage.setItem("accessToken", accessToken)
      this.user = await services.getMe()
      this.loggedIn = true
    },
    async signup(user: UserCreate) {
      try {
        await services.signup(this.adaptToServer(user))
        await this.login(user)
      } catch (e) {
        if (e instanceof BadRequest) {
          toast.warning("Пользователь с таким email уже существует.")
          return
        }

        throw e
      }
    },
    async login(user: UserLogin) {
      try {
        const data = await services.login(user)
        await this.onLogin(data)
      } catch (e) {
        if (e instanceof Unauthorized) {
          toast.warning("Неправильный email и/или пароль.")
          return
        }

        throw e
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
        if (e instanceof TokenExpired) {
          storage.removeItem("accessToken")
          client.removeToken()
          return false
        }

        throw e
      }
    },
    adaptToServer(user: UserCreate): UserCreateServer {
      return {
        email: user.email,
        password: user.password,
        re_password: user.repeatPassword,
      }
    },
  },
})
