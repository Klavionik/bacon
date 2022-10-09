import { defineStore } from "pinia/dist/pinia"
import api from "@/services/api"
import { useUserStore } from "@/stores/user"
import type { Treat } from "@/models/treat"

export const useTreatsStore = defineStore("treats", {
  state: () => {
    return {
      treats: [] as Array<Treat>,
    }
  },
  actions: {
    adaptFromServer(treat: any): Treat {
      return {
        id: treat["id"],
        title: treat["title"],
        available: treat["available"],
        price: treat["price"],
        oldPrice: treat["old_price"],
        url: treat["url"],
        shopTitle: treat["shop_display_title"],
        shopId: treat["shop_id"],
      }
    },
    async fetchTreats() {
      const userStore = useUserStore()
      this.treats = (await api.listUserTreats(userStore.user.id)).map(this.adaptFromServer)
    },
    async createTreat(url: string) {
      const userStore = useUserStore()
      let treat = await api.createTreat(url, userStore.user.id)
      treat = this.adaptFromServer(treat)
      this.treats.push(treat)
    },
    async deleteTreat(id: number) {
      const response = await api.deleteTreat(id)

      if (response.status !== 204) {
        throw Error(`Cannot delete treat with id ${id}.`)
      }

      this.treats = this.treats.filter((treat) => treat.id !== id)
    },
  },
})
