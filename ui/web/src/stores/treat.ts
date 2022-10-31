import { defineStore } from "pinia/dist/pinia"
import api from "@/services/api"
import type { Treat } from "@/models/treat"

export const useTreatsStore = defineStore("treat", {
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
    async fetchTreats(userId: number) {
      this.treats = (await api.listUserTreats(userId)).map(this.adaptFromServer)
    },
    async create(userId: number, url: string) {
      let treat = await api.createTreat(userId, url)
      treat = this.adaptFromServer(treat)
      this.treats.push(treat)
    },
    async delete(id: number) {
      const response = await api.deleteTreat(id)

      if (response.status !== 204) {
        throw Error(`Cannot delete treat with id ${id}.`)
      }

      this.treats = this.treats.filter((treat) => treat.id !== id)
    },
  },
})
