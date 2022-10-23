<template>
  <div class="width-75 mx-auto my-2">
    <div class="card p-4">
      <h1 class="is-size-4 has-text-centered">Профиль</h1>
      <hr />
      <div class="card-content">
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
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import VueSelect from "vue-select"
import debounce from "lodash.debounce"
import { defineComponent } from "vue"
import { useShopLocationsStore } from "@/stores/shop-locations"
import type { ShopLocation } from "@/models/shop"
import { useShopsStore } from "@/stores/shops"

export default defineComponent({
  name: "UserProfile",
  components: { VueSelect },
  setup() {
    const shopsStore = useShopsStore()
    const shopLocationsStore = useShopLocationsStore()
    return { shopsStore, shopLocationsStore }
  },
  data() {
    return {
      saving: false,
      saved: false,
      choosenShopLocations: new Map() as Map<number, ShopLocation | null>,
      shopLocationOptions: [] as Array<ShopLocation>,
      fetchOptions: null as any,
      user: this.$auth0.idTokenClaims,
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
        await this.shopLocationsStore.saveUserShopLocations(this.user.sub, locations)
      } finally {
        this.saving = false
        this.showSavedNotification()
      }
      // this.setChoosenShopLocations(this.shopLocationsStore.userShopLocations)
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
.width-75 {
  width: 75%;
}

hr {
  margin: 0.5rem;
}

.is-absolute {
  position: absolute;
}
</style>
