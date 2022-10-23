<template>
  <NavBar />
  <section class="hero">
    <div class="hero-body">
      <p class="title">Вкусняшки</p>
      <p class="subtitle has-text-danger">Пора купить!</p>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "@/components/NavBar.vue"

export default defineComponent({
  name: "HomeView",
  components: { NavBar },
})
</script>

<style scoped></style>
