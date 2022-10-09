import { defineStore } from "pinia"
import type { Shop } from "@/models/shop"
import api from "@/services/api"

export const useShopsStore = defineStore("shops", {
  state: () => {
    return {
      shops: [] as Array<Shop>,
    }
  },
  getters: {
    shopUrlRules(): Array<RegExp> {
      return this.shops.map((shop) => new RegExp(shop["urlRule"]))
    },
  },
  actions: {
    async fetchShops() {
      this.shops = (await api.listShops()).map(this.adaptFromServer)
    },
    adaptFromServer(shop: any): Shop {
      return {
        id: shop["id"],
        title: shop["title"],
        displayTitle: shop["display_title"],
        urlRule: shop["url_rule"],
      }
    },
  },
})
