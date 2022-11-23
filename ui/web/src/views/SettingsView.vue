<template>
  <NavBar />
  <div class="card p-4">
    <h1 class="is-size-4 has-text-centered">Настройки</h1>
    <div class="card-content">
      <AppTabs
        :tabs="settingsTabs"
        :active-tab="activeTab"
        :fullwidth="true"
        :boxed="true"
        @update:tab="navigate"
      />
      <RouterView />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { settingsTabs } from "@/consts"
import NavBar from "@/components/NavBar.vue"
import AppTabs from "@/components/AppTabs.vue"

export default defineComponent({
  name: "SettingsView",
  components: { NavBar, AppTabs },
  data() {
    return {
      settingsTabs,
    }
  },
  computed: {
    activeTab() {
      if (typeof this.$route?.name !== "string") {
        throw Error("Route has no name.")
      }
      return this.$route.name
    },
  },
  methods: {
    navigate(tabId: string) {
      this.$router.push({ name: tabId })
    },
  },
})
</script>

<style scoped>
.card {
  border-top-right-radius: 0;
  border-top-left-radius: 0;
}
</style>
