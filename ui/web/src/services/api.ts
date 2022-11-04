import type { ShopLocation } from "@/models/shop"
import { BaseHTTPService } from "@/services/http"

class APIService extends BaseHTTPService {
  async listShops(): Promise<Array<any>> {
    const response = await this._get("shops")
    return response.json()
  }

  async listUserTreats(userId: number): Promise<Array<any>> {
    const options = { searchParams: { user_id: userId } }
    const response = await this._get("treats", options)
    return response.json()
  }

  async createTreat(userId: number, url: string): Promise<any> {
    const options = { json: { url }, searchParams: { user_id: userId } }
    const response = await this._post("treats", options)
    return response.json()
  }

  deleteTreat(id: number): Promise<any> {
    return this._delete(`treats/${id}`)
  }

  async searchShopLocations(shopId: number, address: string): Promise<Array<any>> {
    const options = { searchParams: { address } }
    const response = await this._get(`shops/${shopId}/locations/search`, options)
    return response.json()
  }

  async getUserShopLocations(userId: number): Promise<Array<ShopLocation>> {
    const response = await this._get(`user/${userId}/shop-locations`)
    return response.json()
  }

  async saveUserShopLocations(userId: number, locations: Array<any>): Promise<Array<any>> {
    const options = { json: locations }
    const response = await this._put(`user/${userId}/shop-locations`, options)
    return response.json()
  }
}

export default new APIService(import.meta.env.VITE_API_URL, "api")
