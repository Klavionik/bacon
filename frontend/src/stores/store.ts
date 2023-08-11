import { defineStore } from "pinia"
import type { ShopLocation, StoreSearchSuggestion } from "@/models/shop"
import { services } from "@/http"

export const useStoreStore = defineStore("store", {
  state: () => {
    return {
      userShopLocations: new Map() as Map<number, ShopLocation | null>,
    }
  },
  getters: {
    noShopLocationsConfigured(): boolean {
      return !this.userShopLocations.size
    },
  },
  actions: {
    adaptFromServer(location: any): [number, ShopLocation] {
      return [
        location["store"]["retailer"],
        {
          id: location.id,
          title: location["store"]["title"],
          address: location["store"]["address"],
          externalId: location["store"]["external_id"],
        },
      ]
    },
    adaptSuggestionFromServer(suggestion: any): StoreSearchSuggestion {
      return {
        title: suggestion["title"],
        address: suggestion["address"],
        externalId: suggestion["external_id"],
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
    ): Promise<Array<StoreSearchSuggestion>> {
      const locations = await services.searchShopLocations(shopId, address)
      return locations.map(this.adaptSuggestionFromServer)
    },
    async fetchUserShopLocations() {
      const locations = await services.getUserShopLocations()
      this.userShopLocations = new Map(locations.map(this.adaptFromServer))
    },
    async saveUserShopLocation(retailerId: number, updatedLocation: ShopLocation | null) {
      if (updatedLocation === null) {
        const userShopLocation = this.userShopLocations.get(retailerId)
        await services.deleteUserShopLocation(userShopLocation!.id)
      } else {
        await services.saveUserShopLocation(this.adaptToServer(retailerId, updatedLocation))
      }

      await this.fetchUserShopLocations()
    },
    isShopLocationConfigured(shopId: number) {
      return this.userShopLocations.has(shopId)
    },
  },
})
