export type Shop = {
  id: number
  title: string
  displayTitle: string
  urlRule: string
}

export type ShopLocation = {
  id: number
  title: string
  address: string
  externalId: number
  shopId?: number
}

export type StoreSearchSuggestion = {
  title: string
  address: string
  externalId: number
}
