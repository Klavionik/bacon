import { defineStore } from "pinia"
import type { ShopLocation, StoreSearchSuggestion } from "@/models/shop"
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
        title: location["store"]["title"],
        address: location["store"]["address"],
        externalId: location["store"]["external_id"],
        shopId: location["store"]["retailer"],
      }
    },
    adaptToServer(retailerId: number, location: StoreSearchSuggestion) {
      return {
        store: {
          title: location.title,
          address: location.address,
          external_id: location.externalId,
          retailer: retailerId,
        },
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
      const locations = await services.getUserShopLocations()
      this.userShopLocations = locations.map(this.adaptFromServer)
    },
    async saveUserShopLocation(retailerId: number, updatedLocation: ShopLocation) {
      await services.saveUserShopLocation(this.adaptToServer(retailerId, updatedLocation))
      await this.fetchUserShopLocations()
    },
    isShopLocationConfigured(shopId: number) {
      return this.userShopLocations.some((location) => location.shopId === shopId)
    },
  },
})
