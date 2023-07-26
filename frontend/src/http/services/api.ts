import type { ShopLocation } from "@/models/shop"
import type { HTTPService } from "@/http/services/types"
import type { HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

export class APIService implements HTTPService {
  client
  prefix = "api/v1/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async listShops(): Promise<Array<any>> {
    const response = await this.client.get("retailers/")
    return response.json()
  }

  async listProducts(): Promise<Array<any>> {
    const response = await this.client.get("userproducts/")
    return response.json()
  }

  async createProduct(product: any): Promise<any> {
    const options = { json: product }
    const response = await this.client.post("userproducts/", options)
    return response.json()
  }

  deleteProduct(id: number): Promise<any> {
    return this.client.delete(`user_products/${id}`)
  }

  async searchShopLocations(shopId: number, address: string): Promise<Array<any>> {
    const options = { searchParams: { term: address } }
    const response = await this.client.get(`retailers/${shopId}/stores/search/`, options)
    return response.json()
  }

  async getUserShopLocations(): Promise<Array<ShopLocation>> {
    const response = await this.client.get(`userstores/`)
    return response.json()
  }

  async saveUserShopLocation(location: any): Promise<any> {
    const options = { json: location }
    const response = await this.client.post(`userstores/`, options)
    return response.json()
  }
}
