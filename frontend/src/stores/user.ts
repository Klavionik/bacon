import { defineStore } from "pinia"
import type { UserCreate, UserCreateServer, UserLogin, UserRead } from "@/models/user"
import { services, client } from "@/http/"
import storage from "@/storage"
import { BadRequest, Unauthorized } from "@/http/errors"
import { useToast } from "vue-toastification"
import { isJWTExpired } from "@/utils"

const toast = useToast()

export class TokenExpired extends Error {}

export class NoAccessToken extends Error {}

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      user: {} as UserRead,
      loggedIn: false,
      accessToken: "",
    }
  },
  actions: {
    isTokenExpired(): boolean {
      return !this.accessToken || isJWTExpired(this.accessToken)
    },
    async onLogin(token: string) {
      this.accessToken = token
      client.setToken(token)
      storage.setItem("accessToken", token)
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
        await this.onLogin(data["access"])
      } catch (e) {
        if (e instanceof Unauthorized) {
          toast.warning("Неправильный email и/или пароль.")
          return
        }

        throw e
      }
    },
    logout() {
      client.removeToken()
      this.user = {} as UserRead
      this.loggedIn = false
      this.accessToken = ""
      storage.removeItem("accessToken")
    },
    async restoreSession() {
      const savedToken = storage.getItem("accessToken")

      if (savedToken === null) {
        throw new NoAccessToken("No access token")
      }

      if (isJWTExpired(savedToken)) {
        storage.removeItem("accessToken")
        throw new TokenExpired("Access token has expired")
      }

      await this.onLogin(savedToken)
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
