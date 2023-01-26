import { defineStore } from "pinia/dist/pinia"
import { services } from "@/http"
import type { Product } from "@/models/product"

export const useProductsStore = defineStore("product", {
  state: () => {
    return {
      products: [] as Array<Product>,
    }
  },
  actions: {
    adaptFromServer(item: any): Product {
      return {
        id: item["id"],
        title: item["title"],
        available: item["available"],
        price: item["price"],
        oldPrice: item["old_price"],
        url: item["url"],
        shopTitle: item["shop_display_title"],
        shopId: item["shop_id"],
      }
    },
    async fetchProducts(userId: number) {
      this.products = (await services.listProducts(userId)).map(this.adaptFromServer)
    },
    async create(userId: number, url: string) {
      let product = await services.createProduct(userId, url)
      product = this.adaptFromServer(product)
      this.products.push(product)
    },
    async delete(id: number) {
      const response = await services.deleteProduct(id)

      if (response.status !== 204) {
        throw Error(`Cannot delete user product with id ${id}.`)
      }

      this.products = this.products.filter((item) => item.id !== id)
    },
  },
})
