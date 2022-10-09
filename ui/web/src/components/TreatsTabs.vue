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

export default defineComponent({
  name: "TreatsTabs",
  props: {
    activeTab: {
      type: String,
      default: "ALL",
    },
  },
  emits: ["switch"],
  data() {
    return {
      tabs: ["ALL", "DISCOUNTED"],
    }
  },
})
</script>
