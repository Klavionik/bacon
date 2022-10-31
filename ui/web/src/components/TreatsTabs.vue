<template>
  <p class="panel-tabs">
    <a
      v-for="tab in tabs"
      :key="tab"
      href=""
      :class="{ 'is-active': tab === activeTab }"
      @click.prevent="$emit('switch', tab)"
      >{{ tab }}</a
    >
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { mapState } from "pinia"
import { useShopsStore } from "@/stores/shop"

export default defineComponent({
  name: "TreatsTabs",
  props: {
    activeTab: {
      type: String,
      default: "Все",
    },
  },
  emits: ["switch"],
  computed: {
    ...mapState(useShopsStore, ["shops"]),
    tabs() {
      const shopTabs = this.shops.map((shop) => shop.displayTitle)
      return ["Все", "Со скидкой", ...shopTabs]
    },
  },
})
</script>
