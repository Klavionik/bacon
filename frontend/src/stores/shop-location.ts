import { defineStore } from "pinia"
import type { ShopLocation } from "@/models/shop"
import { services } from "@/http"
import { useUserStore } from "@/stores/user"

export const useShopLocationsStore = defineStore("shopLocation", {
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
      const locations = await services.searchShopLocations(shopId, address)
      return locations.map(this.adaptFromServer)
    },
    async fetchUserShopLocations() {
      const { user } = useUserStore()
      const locations = await services.getUserShopLocations(user.id)
      this.userShopLocations = locations.map(this.adaptFromServer)
    },
    async saveUserShopLocations(updatedLocations: Array<ShopLocation>) {
      const { user } = useUserStore()
      const locations = await services.saveUserShopLocations(
        user.id,
        updatedLocations.map(this.adaptToServer)
      )
      this.userShopLocations = locations.map(this.adaptFromServer)
    },
    isShopLocationConfigured(shopId: number) {
      return this.userShopLocations.some((location) => location.shopId === shopId)
    },
  },
})
