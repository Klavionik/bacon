<template>
  <NavBar />
  <main>
    <RouterView />
  </main>
  <AppFooter />
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import NavBar from "@/components/NavBar.vue"
import AppFooter from "@/components/AppFooter.vue"

export default defineComponent({
  name: "AppLayout",
  components: { AppFooter, RouterView, NavBar },
})
</script>

<style scoped></style>
