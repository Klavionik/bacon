import type { ShopLocation } from "@/models/shop"
import type { HTTPService } from "@/http/services/types"
import type { HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

export class APIService implements HTTPService {
  client
  prefix = "api/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async listShops(): Promise<Array<any>> {
    const response = await this.client.get("shops")
    return response.json()
  }

  async listProducts(userId: number): Promise<Array<any>> {
    const options = { searchParams: { user_id: userId } }
    const response = await this.client.get("user_products", options)
    return response.json()
  }

  async createProduct(userId: number, url: string): Promise<any> {
    const options = { json: { url }, searchParams: { user_id: userId } }
    const response = await this.client.post("user_products", options)
    return response.json()
  }

  deleteProduct(id: number): Promise<any> {
    return this.client.delete(`user_products/${id}`)
  }

  async searchShopLocations(shopId: number, address: string): Promise<Array<any>> {
    const options = { searchParams: { address } }
    const response = await this.client.get(`shops/${shopId}/locations/search`, options)
    return response.json()
  }

  async getUserShopLocations(userId: number): Promise<Array<ShopLocation>> {
    const response = await this.client.get(`user/${userId}/shop-locations`)
    return response.json()
  }

  async saveUserShopLocations(userId: number, locations: Array<any>): Promise<Array<any>> {
    const options = { json: locations }
    const response = await this.client.put(`user/${userId}/shop-locations`, options)
    return response.json()
  }
}
