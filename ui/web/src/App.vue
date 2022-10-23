<template>
  <div class="container">
    <AppLoading v-if="isLoading" />
    <RouterView v-else />
  </div>
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import api from "@/services/api"
import AppLoading from "@/components/AppLoading.vue"
import { useShopsStore } from "@/stores/shops"
import { useShopLocationsStore } from "@/stores/shop-locations"

export default defineComponent({
  name: "App",
  components: { AppLoading, RouterView },
  data() {
    return {
      isLoading: this.$auth0.isLoading,
      isAuthenticated: this.$auth0.isAuthenticated,
      user: this.$auth0.idTokenClaims,
    }
  },
  watch: {
    async isLoading(loading) {
      if (loading) return

      if (this.isAuthenticated) {
        const accessToken = await this.$auth0.getAccessTokenSilently()
        api.setToken(accessToken)

        const shopLocationsStore = useShopLocationsStore()
        await shopLocationsStore.fetchUserShopLocations(this.user.sub)
        const shopsStore = useShopsStore()
        await shopsStore.fetchShops()
      }
    },
  },
})
</script>
