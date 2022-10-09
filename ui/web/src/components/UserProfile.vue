<template>
  <div class="profile-wrapper">
    <div class="card p-2">
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
          <button class="button mt-3 mx-auto" @click.prevent="saveShopLocations">Сохранить</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import VueSelect from "vue-select"
import debounce from "lodash.debounce"
import { useUserStore } from "@/stores/user"
import { defineComponent } from "vue"
import { useShopLocationsStore } from "@/stores/shop-locations"
import type { Shop, ShopLocation } from "@/models/shop"
import { useShopsStore } from "@/stores/shops"

export default defineComponent({
  name: "UserProfile",
  components: { VueSelect },
  setup() {
    const shopsStore = useShopsStore()
    const shopLocationsStore = useShopLocationsStore()
    const userStore = useUserStore()
    return { shopsStore, shopLocationsStore, userStore }
  },
  data() {
    return {
      choosenShopLocations: new Map() as Map<number, ShopLocation | null>,
      shopLocationOptions: [] as Array<ShopLocation>,
      fetchOptions: null as any,
    }
  },
  async mounted() {
    const userShopLocations = await this.shopLocationsStore.fetchUserShopLocations(
      this.userStore.user.id
    )
    this.setChoosenShopLocations(userShopLocations)
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

      const savedLocations = await this.shopLocationsStore.saveUserShopLocations(
        this.userStore.user.id,
        locations
      )
      this.setChoosenShopLocations(savedLocations)
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
  },
})
</script>

<style scoped>
.profile-wrapper {
  width: 50%;
  margin: 0.5rem auto;
}

hr {
  margin: 0.5rem;
}
</style>
