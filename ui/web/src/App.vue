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

export default defineComponent({
  name: "App",
  components: { AppLoading, RouterView },
  data() {
    return {
      isLoading: this.$auth0.isLoading,
    }
  },
  watch: {
    async isLoading(loading) {
      if (loading) return

      if (this.$auth0.isAuthenticated) {
        const accessToken = await this.$auth0.getAccessTokenSilently()
        api.setToken(accessToken)
      }
    },
  },
  async beforeMount() {
    const shopsStore = useShopsStore()
    await shopsStore.fetchShops()
  },
})
</script>
