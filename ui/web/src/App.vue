<template>
  <div class="container">
    <AppLoading v-if="isLoading" />
    <RouterView v-else />
  </div>
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import { useUserStore } from "@/stores/users"
import AppLoading from "@/components/AppLoading.vue"
import { useShopLocationsStore } from "@/stores/shop-locations"
import { useShopsStore } from "@/stores/shops"
import storage from "@/services/storage"

export default defineComponent({
  name: "App",
  components: { AppLoading, RouterView },
  data() {
    return {
      isLoading: false,
    }
  },
  async created() {
    const token = storage.getItem("accessToken")

    if (token) {
      this.isLoading = true
      try {
        const userStore = useUserStore()
        await userStore.loginByToken(token)
        const shopLocationsStore = useShopLocationsStore()
        await shopLocationsStore.fetchUserShopLocations(userStore.user.id)
        const shopsStore = useShopsStore()
        await shopsStore.fetchShops()
      } finally {
        this.isLoading = false
      }
    }
  },
})
</script>
