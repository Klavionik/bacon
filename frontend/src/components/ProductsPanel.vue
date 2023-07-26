<template>
  <div class="panel">
    <ProductSearch v-model:search="search" />
    <ProductTabs :active-tab="activeTab" @switch="activeTab = $event" />
    <template v-if="noShopsConfigured">
      <div class="panel-block is-justify-content-center">
        <article class="message is-small is-warning mb-0">
          <div class="message-body">
            Прежде чем начать добавлять товары, нужно
            <RouterLink :to="{ name: 'shops' }">выбрать магазины</RouterLink>, в которых мы будем
            следить за ценами.
          </div>
        </article>
      </div>
    </template>
    <template v-else-if="filteredProducts.length">
      <ProductItem
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        :is-deleting="isDeleting(product.id)"
        @delete="deleteProduct"
      />
    </template>
    <template v-else>
      <div class="panel-block">
        {{ emptyText }}
      </div>
    </template>
    <NewProduct v-model:url="newProductURL" :is-loading="isCreating" @submit="createProduct" />
  </div>
</template>

<script lang="ts">
import ProductItem from "./ProductItem.vue"
import ProductTabs from "./ProductTabs.vue"
import ProductSearch from "./ProductSearch.vue"
import NewProduct from "./NewProduct.vue"
import { useProductsStore } from "@/stores/treat"
import { defineComponent } from "vue"
import type { Product } from "@/models/product"
import { useShopLocationsStore } from "@/stores/shop-location"
import { RouterLink } from "vue-router"
import { useUserStore } from "@/stores/user"
import { mapState, mapActions } from "pinia"

const notFound = "Ни одного товара не найдено"
const empty = "Пока не добавлено ни одного товара"

export default defineComponent({
  name: "ProductsPanel",
  components: {
    NewProduct,
    ProductItem,
    ProductTabs,
    ProductSearch,
    RouterLink,
  },
  data() {
    return {
      isCreating: false,
      deleting: [] as number[],
      search: "",
      activeTab: "Все",
      newProductURL: "",
    }
  },
  computed: {
    ...mapState(useUserStore, ["user"]),
    ...mapState(useProductsStore, ["products"]),
    ...mapState(useShopLocationsStore, ["userShopLocations"]),
    filteredProducts(): Array<Product> {
      return this.products.filter(this.filterBySearch).filter(this.filterByTab)
    },
    emptyText(): string {
      return this.products.length ? notFound : empty
    },
    noShopsConfigured(): boolean {
      return !this.userShopLocations.length
    },
  },
  methods: {
    ...mapActions(useProductsStore, ["create", "delete"]),
    isDeleting(productId: number) {
      return this.deleting.includes(productId)
    },
    filterBySearch(product: Product): boolean {
      if (!this.search) return true
      return product.title.toLowerCase().includes(this.search.toLowerCase())
    },
    filterByTab(product: Product): boolean {
      const discounted = (treat: Product) => treat.oldPrice !== null && treat.price < treat.oldPrice

      switch (this.activeTab) {
        case "Все":
          return true
        case "Со скидкой":
          return discounted(product)
        default:
          return product.shopTitle === this.activeTab
      }
    },
    async createProduct() {
      this.isCreating = true
      let error = false

      try {
        await this.create(this.newProductURL)
      } catch (e) {
        error = true
        throw e
      } finally {
        this.isCreating = false

        if (!error) this.newProductURL = ""
      }
    },
    async deleteProduct(id: number) {
      this.deleting.push(id)

      try {
        await this.delete(id)
      } finally {
        this.deleting = this.deleting.filter((id_) => id_ !== id)
      }
    },
  },
})
</script>

<style scoped>
.panel {
  border-radius: 0;
}
</style>
