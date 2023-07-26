export type Product = {
  id: number
  title: string
  available: boolean
  url: string
  price: number
  oldPrice: number | null
  shopTitle: string
  shopId: number
}

export type ProductCreate = {
  product: {
    url: string
  }
}
