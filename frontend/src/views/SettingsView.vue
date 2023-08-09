<template>
  <AppSection>
    <div class="card p-4" :class="{ 'no-shadow': isMobile }">
      <h1 class="is-size-4 has-text-centered">Настройки</h1>
      <div class="card-content" :class="{ 'p-0': isMobile }">
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
  </AppSection>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { settingsTabs } from "@/consts"
import AppTabs from "@/components/AppTabs.vue"
import AppSection from "@/components/AppSection.vue"
import { useIsMobile } from "@/utils"

export default defineComponent({
  name: "SettingsView",
  components: { AppSection, AppTabs },
  data() {
    return {
      settingsTabs,
      isMobile: useIsMobile(),
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
