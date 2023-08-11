<template>
  <form class="is-flex is-flex-direction-column">
    <div v-for="retailer in retailerStore.shops" :key="retailer.id" class="field mt-3">
      Выберите адрес вашего магазина <b>{{ retailer.displayTitle }}</b
      >.
      <div class="control mt-2">
        <VueSelect
          :disabled="saving"
          :model-value="storeStore.userStores.get(retailer.id)"
          :options="storeOptions"
          :filterable="false"
          placeholder="Поиск"
          :get-option-label="getStoreOptionLabel"
          @search="(search: string, loading: () => void) => fetchOptions(retailer.id, search, loading)"
          @update:model-value="updateStore(retailer.id, $event)"
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
import { useRetailerStore } from "@/stores/retailer"
import { useStoreStore } from "@/stores/store"
import { settingsTabs } from "@/consts"
import type { ShopLocation, StoreSearchSuggestion } from "@/models/shop"
import debounce from "lodash.debounce"
import { useProgress } from "@marcoschulte/vue3-progress"
import { mapStores } from "pinia"
import { useToast } from "vue-toastification"

const toast = useToast()

export default defineComponent({
  name: "UserShops",
  components: { VueSelect },
  async beforeRouteEnter() {
    const retailerStore = useRetailerStore()
    const storeStore = useStoreStore()
    const promise = Promise.all([retailerStore.fetchShops(), storeStore.fetchUserStores()])
    await useProgress().attach(promise)
  },
  data() {
    return {
      settingsTabs,
      saving: false,
      saved: false,
      storeOptions: [] as Array<StoreSearchSuggestion>,
      fetchOptions: null as any,
      unsubscribe: () => {},
    }
  },
  computed: mapStores(useRetailerStore, useStoreStore),
  async mounted() {
    this.fetchOptions = debounce(this._fetchOptions, 800)
  },
  beforeUnmount() {
    this.fetchOptions.cancel()
    this.unsubscribe()
  },
  methods: {
    clearOptions() {
      this.storeOptions = []
    },
    async updateStore(retailerId: number, store: ShopLocation | null) {
      this.saving = true

      try {
        await this.storeStore.saveUserStore(retailerId, store)
        toast.success("Магазин обновлен.")
      } catch (e) {
        toast.warning("Не удалось обновить магазин.")
        throw e
      } finally {
        this.saving = false
      }
    },
    getStoreOptionLabel(store: ShopLocation) {
      return `${store.address} (${store.title})`
    },
    async _fetchOptions(retailerId: number, search: string, loading: Function) {
      if (!search) return

      loading(true)

      try {
        this.storeOptions = await this.storeStore.fetchStoreSuggestions(retailerId, search)
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
