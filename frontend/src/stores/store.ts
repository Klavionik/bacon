import { defineStore } from "pinia"
import type { ShopLocation, StoreSearchSuggestion } from "@/models/shop"
import { services } from "@/http"

export const useStoreStore = defineStore("store", {
  state: () => {
    return {
      userStores: new Map() as Map<number, ShopLocation | null>,
    }
  },
  getters: {
    noUserStoreConfigured(): boolean {
      return !this.userStores.size
    },
  },
  actions: {
    adaptFromServer(userstore: any): [number, ShopLocation] {
      return [
        userstore["store"]["retailer"],
        {
          id: userstore.id,
          title: userstore["store"]["title"],
          address: userstore["store"]["address"],
          externalId: userstore["store"]["external_id"],
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
    adaptToServer(retailerId: number, storeSuggestion: StoreSearchSuggestion) {
      return {
        store: {
          title: storeSuggestion.title,
          address: storeSuggestion.address,
          external_id: storeSuggestion.externalId,
          retailer: retailerId,
        },
      }
    },
    async fetchStoreSuggestions(
      shopId: number,
      address: string
    ): Promise<Array<StoreSearchSuggestion>> {
      const stores = await services.searchStores(shopId, address)
      return stores.map(this.adaptSuggestionFromServer)
    },
    async fetchUserStores() {
      const stores = await services.getUserStores()
      this.userStores = new Map(stores.map(this.adaptFromServer))
    },
    async saveUserStore(retailerId: number, updatedStore: ShopLocation | null) {
      if (updatedStore === null) {
        const userStore = this.userStores.get(retailerId)
        await services.deleteUserStore(userStore!.id)
      } else {
        await services.saveUserStore(this.adaptToServer(retailerId, updatedStore))
      }

      await this.fetchUserStores()
    },
    isStoreConfigured(retailerId: number) {
      return this.userStores.has(retailerId)
    },
  },
})
