<template>
  <form class="is-flex is-flex-direction-column">
    <div class="field">
      Выберите магазины, в которых станет возможным отслеживание вкусняшек.
      <div class="control mt-3">
        <label v-for="shop in shopStore.shops" :key="shop.id" class="checkbox">
          <input
            type="checkbox"
            :checked="isShopChecked(shop.id)"
            :value="shop.id"
            :disabled="saving"
            @input="updateShop($event, shop.id)"
          />
          {{ shop.displayTitle }}
        </label>
      </div>
    </div>
    <template v-if="choosenShopLocations.size > 0">
      <hr />
      <div v-for="shopId in choosenShopLocations.keys()" :key="shopId" class="field mt-3">
        Выберите адрес вашего магазина
        <strong>{{ getShopNameById(shopId) }}</strong>
        <div class="control mt-1">
          <VueSelect
            :disabled="saving"
            :model-value="choosenShopLocations.get(shopId)"
            :options="shopLocationOptions"
            :filterable="false"
            placeholder="Поиск"
            :get-option-label="getShopLocationOptionLabel"
            @search="(search: string, loading: () => void) => fetchOptions(shopId, search, loading)"
            @update:model-value="updateShopLocation(shopId, $event)"
          >
            <template #no-options> Нет результатов </template>
          </VueSelect>
        </div>
      </div>
    </template>
    <div class="field mt-3 mx-auto">
      <div class="control">
        <button class="button" :disabled="saving" @click.prevent="saveShopLocations">
          Сохранить
        </button>
      </div>
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
import type { ShopLocation } from "@/models/shop"
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
      choosenShopLocations: new Map() as Map<number, ShopLocation | null>,
      shopLocationOptions: [] as Array<ShopLocation>,
      fetchOptions: null as any,
      unsubscribe: () => {},
    }
  },
  computed: mapStores(useShopsStore, useShopLocationsStore),
  async mounted() {
    this.unsubscribe = this.shopLocationStore.$subscribe((mutation, state) => {
      this.setChoosenShopLocations(state.userShopLocations)
    })

    this.setChoosenShopLocations(this.shopLocationStore.userShopLocations)
    this.fetchOptions = debounce(this._fetchOptions, 800)
  },
  beforeUnmount() {
    this.fetchOptions.cancel()
    this.unsubscribe()
  },
  methods: {
    setChoosenShopLocations(shopLocations: Array<ShopLocation>) {
      this.choosenShopLocations = new Map(
        shopLocations.map((location) => {
          return [location.shopId, location]
        })
      )
    },
    isShopChecked(shopId: number): boolean {
      return this.choosenShopLocations.has(shopId)
    },
    updateShopLocation(shopId: number, shopLocation: ShopLocation | null) {
      this.choosenShopLocations.set(shopId, shopLocation)
      this.shopLocationOptions = []
    },
    updateShop(event: Event, shopId: number) {
      const target = event.target as HTMLInputElement

      if (target.checked) {
        this.choosenShopLocations.set(shopId, null)
      } else {
        this.choosenShopLocations.delete(shopId)
      }
    },
    getShopNameById(id: number) {
      return this.shopStore.shops.find((shop) => shop.id === id)?.displayTitle
    },
    getShopLocationOptionLabel(shopLocation: ShopLocation) {
      return `${shopLocation.address} (${shopLocation.title})`
    },
    async saveShopLocations() {
      const locations = Array.from(this.choosenShopLocations.values()).filter(
        (value) => value !== null
      ) as Array<ShopLocation>

      this.saving = true

      try {
        await this.shopLocationStore.saveUserShopLocations(locations)
      } finally {
        this.saving = false
        this.showSavedNotification()
      }
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
    showSavedNotification() {
      this.saved = true
      setTimeout(() => (this.saved = false), 2000)
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
