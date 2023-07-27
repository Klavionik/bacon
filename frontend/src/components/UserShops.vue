<template>
  <form class="is-flex is-flex-direction-column">
    <div v-for="shop in shopStore.shops" :key="shop.id" class="field mt-3">
      Выберите адрес вашего магазина <b>{{ shop.displayTitle }}</b
      >.
      <div class="control mt-2">
        <VueSelect
          :disabled="saving"
          :model-value="shopLocationStore.userShopLocations.get(shop.id)"
          :options="shopLocationOptions"
          :filterable="false"
          placeholder="Поиск"
          :get-option-label="getShopLocationOptionLabel"
          @search="(search: string, loading: () => void) => fetchOptions(shop.id, search, loading)"
          @update:model-value="updateShopLocation(shop.id, $event)"
          @close="clearOptions"
        >
          <template #no-options> Нет результатов </template>
        </VueSelect>
      </div>
    </div>
    <div class="field mt-3 mx-auto">
      <p v-if="saved" class="help has-text-centered is-absolute">
        <i class="fa-sharp fa-solid fa-circle-check has-text-success"></i>
        Сохранено!
      </p>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import VueSelect from "vue-select"
import { useShopsStore } from "@/stores/shop"
import { useShopLocationsStore } from "@/stores/shop-location"
import { settingsTabs } from "@/consts"
import type { ShopLocation, StoreSearchSuggestion } from "@/models/shop"
import debounce from "lodash.debounce"
import { useProgress } from "@marcoschulte/vue3-progress"
import { mapStores } from "pinia"

export default defineComponent({
  name: "UserShops",
  components: { VueSelect },
  async beforeRouteEnter() {
    const shopsStore = useShopsStore()
    const shopLocationsStore = useShopLocationsStore()
    const promise = Promise.all([
      shopsStore.fetchShops(),
      shopLocationsStore.fetchUserShopLocations(),
    ])
    await useProgress().attach(promise)
  },
  data() {
    return {
      settingsTabs,
      saving: false,
      saved: false,
      shopLocationOptions: [] as Array<StoreSearchSuggestion>,
      fetchOptions: null as any,
      unsubscribe: () => {},
    }
  },
  computed: mapStores(useShopsStore, useShopLocationsStore),
  async mounted() {
    this.fetchOptions = debounce(this._fetchOptions, 800)
  },
  beforeUnmount() {
    this.fetchOptions.cancel()
    this.unsubscribe()
  },
  methods: {
    clearOptions() {
      this.shopLocationOptions = []
    },
    async updateShopLocation(shopId: number, shopLocation: ShopLocation | null) {
      this.saving = true
      await this.shopLocationStore.saveUserShopLocation(shopId, shopLocation)
      this.saving = false
    },
    getShopLocationOptionLabel(shopLocation: ShopLocation) {
      return `${shopLocation.address} (${shopLocation.title})`
    },
    async _fetchOptions(shopId: number, search: string, loading: Function) {
      if (!search) return

      loading(true)

      try {
        this.shopLocationOptions = await this.shopLocationStore.fetchShopLocationSuggestions(
          shopId,
          search
        )
      } finally {
        loading(false)
      }
    },
  },
})
</script>

<style scoped>
hr {
  margin: 0.5rem;
}

.is-absolute {
  position: absolute;
}
</style>
