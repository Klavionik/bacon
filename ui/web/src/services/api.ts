import type { ResponsePromise } from "ky"
import type { ShopLocation } from "@/models/shop"
import { BaseHTTPService } from "@/services/http"

class APIService extends BaseHTTPService {
  listShops(): Promise<Array<any>> {
    return this.client.get("shops").json()
  }

  listUserTreats(userId: number): Promise<Array<any>> {
    const options = { searchParams: { user_id: userId } }
    return this.client.get("treats", options).json()
  }

  createTreat(userId: number, url: string): Promise<any> {
    const options = { json: { url }, searchParams: { user_id: userId } }
    return this.client.post("treats", options).json()
  }

  deleteTreat(id: number): ResponsePromise {
    return this.client.delete(`treats/${id}`)
  }

  searchShopLocations(shopId: number, address: string): Promise<Array<any>> {
    const options = { searchParams: { address } }
    return this.client.get(`shops/${shopId}/locations/search`, options).json()
  }

  getUserShopLocations(userId: number): Promise<Array<ShopLocation>> {
    return this.client.get(`user/${userId}/shop-locations`).json()
  }

  saveUserShopLocations(userId: number, locations: Array<any>): Promise<Array<any>> {
    const options = { json: locations }
    return this.client.put(`user/${userId}/shop-locations`, options).json()
  }
}

export default new APIService(import.meta.env.VITE_API_URL, "api")
