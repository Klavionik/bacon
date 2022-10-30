<template>
  <form class="is-flex is-flex-direction-column">
    <div class="field">
      Выберите магазины, в которых станет возможным отслеживание вкусняшек.
      <div class="control mt-3">
        <label v-for="shop in shopsStore.shops" :key="shop.id" class="checkbox">
          <input
            type="checkbox"
            :checked="isShopChecked(shop.id)"
            :value="shop.id"
            :disabled="saving"
            @input="updateShop($event.target.checked, shop.id)"
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
            @search="(search, loading) => fetchOptions(shopId, search, loading)"
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
import { useShopsStore } from "@/stores/shops"
import { useShopLocationsStore } from "@/stores/shop-locations"
import { useUserStore } from "@/stores/users"
import { settingsTabs } from "@/consts"
import type { ShopLocation } from "@/models/shop"
import debounce from "lodash.debounce"

export default defineComponent({
  name: "UserShops",
  components: { VueSelect },
  async beforeRouteEnter() {
    const shopsStore = useShopsStore()
    const shopLocationsStore = useShopLocationsStore()
    await Promise.all([shopsStore.fetchShops(), shopLocationsStore.fetchUserShopLocations()])
  },
  setup() {
    const { user } = useUserStore()
    return { user }
  },
  data() {
    return {
      settingsTabs,
      saving: false,
      saved: false,
      choosenShopLocations: new Map() as Map<number, ShopLocation | null>,
      shopLocationOptions: [] as Array<ShopLocation>,
      fetchOptions: null as any,
      shopsStore: useShopsStore(),
      shopLocationsStore: useShopLocationsStore(),
    }
  },
  async mounted() {
    this.shopLocationsStore.$subscribe((mutation, state) => {
      this.setChoosenShopLocations(state.userShopLocations)
    })

    this.setChoosenShopLocations(this.shopLocationsStore.userShopLocations)
    this.fetchOptions = debounce(this._fetchOptions, 800)
  },
  beforeUnmount() {
    this.fetchOptions.cancel()
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
    updateShop(checked: boolean, shopId: number) {
      if (checked) {
        this.choosenShopLocations.set(shopId, null)
      } else {
        this.choosenShopLocations.delete(shopId)
      }
    },
    getShopNameById(id: number) {
      return this.shopsStore.shops.find((shop) => shop.id === id)?.displayTitle
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
        await this.shopLocationsStore.saveUserShopLocations(locations)
      } finally {
        this.saving = false
        this.showSavedNotification()
      }
    },
    async _fetchOptions(shopId: number, search: string, loading: Function) {
      if (!search) return

      loading(true)

      try {
        this.shopLocationOptions = await this.shopLocationsStore.fetchShopLocationSuggestions(
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
