import { defineStore } from "pinia"
import type { Shop } from "@/models/shop"
import api from "@/http/services/api"

export const useShopsStore = defineStore("shop", {
  state: () => {
    return {
      shops: [] as Array<Shop>,
    }
  },
  getters: {
    shopUrlRules(): Array<RegExp> {
      return this.shops.map((shop) => new RegExp(shop.urlRule))
    },
  },
  actions: {
    async fetchShops() {
      this.shops = (await api.listShops()).map(this.adaptFromServer)
    },
    getShopByTreatURL(url: string) {
      return this.shops.find((shop) => {
        const urlRule = new RegExp(shop.urlRule)
        return urlRule.test(url)
      })
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
