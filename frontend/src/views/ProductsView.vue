<template>
  <AppSection :mobile-padding="false">
    <ProductsPanel />
  </AppSection>
</template>

<script lang="ts">
import AppSection from "@/components/AppSection.vue"
import ProductsPanel from "@/components/ProductsPanel.vue"
import { defineComponent } from "vue"
import { useShopsStore } from "@/stores/shop"
import { useProductsStore } from "@/stores/treat"
import { useShopLocationsStore } from "@/stores/shop-location"
import { useProgress } from "@marcoschulte/vue3-progress"

export default defineComponent({
  name: "ProductsView",
  components: { AppSection, ProductsPanel },
  async beforeRouteEnter() {
    const shopsStore = useShopsStore()
    const productsStore = useProductsStore()
    const shopLocationsStore = useShopLocationsStore()
    const promise = Promise.all([
      shopsStore.fetchShops(),
      productsStore.fetchProducts(),
      shopLocationsStore.fetchUserShopLocations(),
    ])
    await useProgress().attach(promise)
  },
})
</script>
