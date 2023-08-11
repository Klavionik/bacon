<template>
  <AppSection>
    <ProductsPanel />
  </AppSection>
</template>

<script lang="ts">
import AppSection from "@/components/AppSection.vue"
import ProductsPanel from "@/components/ProductsPanel.vue"
import { defineComponent } from "vue"
import { useRetailerStore } from "@/stores/retailer"
import { useProductStore } from "@/stores/product"
import { useStoreStore } from "@/stores/store"
import { useProgress } from "@marcoschulte/vue3-progress"

export default defineComponent({
  name: "ProductsView",
  components: { AppSection, ProductsPanel },
  async beforeRouteEnter() {
    const retailerStore = useRetailerStore()
    const productStore = useProductStore()
    const storeStore = useStoreStore()
    const promise = Promise.all([
      retailerStore.fetchShops(),
      productStore.fetchProducts(),
      storeStore.fetchUserShopLocations(),
    ])
    await useProgress().attach(promise)
  },
})
</script>
