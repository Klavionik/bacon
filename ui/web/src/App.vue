<template>
  <div class="container">
    <RouterView />
  </div>
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"

export default defineComponent({
  name: "App",
  components: { RouterView },
})
</script>
