<template>
  <NavBar />
  <TreatsPanel />
</template>

<script lang="ts">
import TreatsPanel from "@/components/TreatsPanel.vue"
import NavBar from "@/components/NavBar.vue"
import { defineComponent } from "vue"

export default defineComponent({
  name: "TreatsView",
  components: { NavBar, TreatsPanel },
})
</script>
