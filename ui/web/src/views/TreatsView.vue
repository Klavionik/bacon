<template>
  <NavBar />
  <TreatsPanel />
</template>

<script lang="ts">
import TreatsPanel from "@/components/TreatsPanel.vue"
import NavBar from "@/components/NavBar.vue"
import { defineComponent } from "vue"
import { useShopsStore } from "@/stores/shops"
import { useTreatsStore } from "@/stores/treats"
import { useShopLocationsStore } from "@/stores/shop-locations"
import { useUserStore } from "@/stores/users"

export default defineComponent({
  name: "TreatsView",
  components: { NavBar, TreatsPanel },
  async beforeRouteEnter() {
    const { user } = useUserStore()
    const shopsStore = useShopsStore()
    const treatsStore = useTreatsStore()
    const shopLocationsStore = useShopLocationsStore()
    await Promise.all([
      shopsStore.fetchShops(),
      treatsStore.fetchTreats(user.id),
      shopLocationsStore.fetchUserShopLocations(),
    ])
  },
})
</script>
