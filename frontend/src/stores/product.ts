import { defineStore } from "pinia/dist/pinia"
import { services } from "@/http"
import type { Product, ProductCreate } from "@/models/product"

export const useProductStore = defineStore("product", {
  state: () => {
    return {
      products: [] as Array<Product>,
    }
  },
  actions: {
    adaptToServer(url: string): ProductCreate {
      return {
        product: {
          url,
        },
      }
    },
    adaptFromServer(item: any): Product {
      const { product } = item
      return {
        id: item["id"],
        title: product["title"],
        available: product["in_stock"],
        price: product["price"]["current"],
        oldPrice: product["price"]["old"],
        url: product["url"],
        shopTitle: product["store"]["retailer"]["display_title"],
        shopId: product["store"]["retailer"]["id"],
      }
    },
    async fetchProducts() {
      this.products = (await services.listProducts()).map(this.adaptFromServer)
    },
    async create(url: string) {
      let product = await services.createProduct(this.adaptToServer(url))
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
