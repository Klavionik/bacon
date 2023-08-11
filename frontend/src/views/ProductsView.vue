<template>
  <AppSection>
    <div v-if="noUserStoreConfigured" class="is-flex pb-2 is-justify-content-center">
      <article class="message is-small is-warning">
        <div class="message-body">
          Прежде чем начать добавлять товары, нужно
          <RouterLink :to="{ name: 'shops' }">выбрать магазины</RouterLink>, в которых мы будем
          следить за ценами.
        </div>
      </article>
    </div>
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
import { mapState } from "pinia"

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
      storeStore.fetchUserStores(),
    ])
    await useProgress().attach(promise)
  },
  computed: mapState(useStoreStore, ["noUserStoreConfigured"]),
})
</script>
