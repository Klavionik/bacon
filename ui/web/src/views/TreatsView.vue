<template>
  <AppSection :mobile-padding="false">
    <TreatsPanel />
  </AppSection>
</template>

<script lang="ts">
import AppSection from "@/components/AppSection.vue"
import TreatsPanel from "@/components/TreatsPanel.vue"
import { defineComponent } from "vue"
import { useShopsStore } from "@/stores/shop"
import { useTreatsStore } from "@/stores/treat"
import { useShopLocationsStore } from "@/stores/shop-location"
import { useUserStore } from "@/stores/user"
import { useProgress } from "@marcoschulte/vue3-progress"

export default defineComponent({
  name: "TreatsView",
  components: { AppSection, TreatsPanel },
  async beforeRouteEnter() {
    const { user } = useUserStore()
    const shopsStore = useShopsStore()
    const treatsStore = useTreatsStore()
    const shopLocationsStore = useShopLocationsStore()
    const promise = Promise.all([
      shopsStore.fetchShops(),
      treatsStore.fetchTreats(user.id),
      shopLocationsStore.fetchUserShopLocations(),
    ])
    await useProgress().attach(promise)
  },
})
</script>
