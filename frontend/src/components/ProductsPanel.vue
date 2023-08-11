<template>
  <div class="panel" :class="{ 'no-shadow': isMobile }">
    <NewProduct v-model:url="newProductURL" :is-loading="isCreating" @submit="createProduct" />
    <ProductTabs :active-tab="activeTab" @switch="activeTab = $event" />
    <ProductSearch v-model:search="search" />
    <template v-if="noUserStoreConfigured">
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
  </div>
</template>

<script lang="ts">
import ProductItem from "./ProductItem.vue"
import ProductTabs from "./ProductTabs.vue"
import ProductSearch from "./ProductSearch.vue"
import NewProduct from "./NewProduct.vue"
import { useProductStore } from "@/stores/product"
import { defineComponent } from "vue"
import type { Product } from "@/models/product"
import { useStoreStore } from "@/stores/store"
import { RouterLink } from "vue-router"
import { useUserStore } from "@/stores/user"
import { mapState, mapActions } from "pinia"
import { useIsMobile } from "@/utils"
import { useToast } from "vue-toastification"
import { Conflict } from "@/http/errors"

const notFound = "Ни одного товара не найдено"
const empty = "Пока не добавлено ни одного товара"

const toast = useToast()
const CONFLICT_WARNING_TIMEOUT_MS = 3000

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
      isMobile: useIsMobile(),
    }
  },
  computed: {
    ...mapState(useUserStore, ["user"]),
    ...mapState(useProductStore, ["products"]),
    ...mapState(useStoreStore, ["userStores", "noUserStoreConfigured"]),
    filteredProducts(): Array<Product> {
      return this.products.filter(this.filterBySearch).filter(this.filterByTab)
    },
    emptyText(): string {
      return this.products.length ? notFound : empty
    },
  },
  methods: {
    ...mapActions(useProductStore, ["create", "delete"]),
    isDeleting(productId: number) {
      return this.deleting.includes(productId)
    },
    filterBySearch(product: Product): boolean {
      if (!this.search) return true
      return product.title.toLowerCase().includes(this.search.toLowerCase())
    },
    filterByTab(product: Product): boolean {
      const discounted = (product: Product) =>
        product.oldPrice !== null && product.price < product.oldPrice

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

      try {
        await this.create(this.newProductURL)
        this.newProductURL = ""
      } catch (e) {
        if (e instanceof Conflict) {
          toast.warning("Этот продукт уже отслеживается.", { timeout: CONFLICT_WARNING_TIMEOUT_MS })
          this.newProductURL = ""
          return
        }

        throw e
      } finally {
        this.isCreating = false
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
