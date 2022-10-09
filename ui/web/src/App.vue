<template>
  <RouterView />
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { useUserStore } from "@/stores/user"
import { useTreatsStore } from "@/stores/treats"
import { defineComponent } from "vue"
import { useShopsStore } from "@/stores/shops"

export default defineComponent({
  name: "App",
  components: { RouterView },
  setup() {
    const userStore = useUserStore()
    const shopsStore = useShopsStore()
    const treatsStore = useTreatsStore()
    return { userStore, shopsStore, treatsStore }
  },
  async mounted() {
    await this.userStore.fetchUser()
    await this.treatsStore.fetchTreats()
    await this.shopsStore.fetchShops()
    this.$router.push({ name: "treats" })
  },
})
</script>
