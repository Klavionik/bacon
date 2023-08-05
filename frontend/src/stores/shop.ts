import { defineStore } from "pinia"
import type { Shop } from "@/models/shop"
import { services } from "@/http"

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
      this.shops = (await services.listShops()).map(this.adaptFromServer)
    },
    getShopByProductURL(url: string) {
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
        urlRule: shop["product_url_pattern"],
      }
    },
  },
})
