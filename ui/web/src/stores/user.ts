import { defineStore } from "pinia/dist/pinia"
import api from "@/services/api"
import type { User } from "@/models/user"

export const useUserStore = defineStore("user", {
  state: () => {
    return {
      user: {} as User,
    }
  },
  actions: {
    async fetchUser() {
      this.user = (await api.getUser()) as User
    },
  },
})
