import { defineStore } from "pinia"
import type { ShopLocation } from "@/models/shop"
import api from "@/services/api"

export const useShopLocationsStore = defineStore("shop-locations", {
  state: () => {
    return {
      userShopLocations: [] as Array<ShopLocation>,
    }
  },
  getters: {
    noShopLocationsConfigured(): boolean {
      return !this.userShopLocations.length
    },
  },
  actions: {
    adaptFromServer(location: any): ShopLocation {
      return {
        title: location["title"],
        address: location["address"],
        externalId: location["external_id"],
        shopId: location["shop_id"],
      }
    },
    adaptToServer(location: ShopLocation) {
      return {
        title: location.title,
        address: location.address,
        external_id: location.externalId,
        shop_id: location.shopId,
      }
    },
    async fetchShopLocationSuggestions(
      shopId: number,
      address: string
    ): Promise<Array<ShopLocation>> {
      const locations = await api.searchShopLocations(shopId, address)
      return locations.map(this.adaptFromServer)
    },
    async fetchUserShopLocations(userId: number) {
      const locations = await api.getUserShopLocations(userId)
      this.userShopLocations = locations.map(this.adaptFromServer)
    },
    async saveUserShopLocations(userId: number, updatedLocations: Array<ShopLocation>) {
      const locations = await api.saveUserShopLocations(
        userId,
        updatedLocations.map(this.adaptToServer)
      )
      this.userShopLocations = locations.map(this.adaptFromServer)
    },
    isShopLocationConfigured(shopId: number) {
      return this.userShopLocations.some((location) => location.shopId === shopId)
    },
  },
})
