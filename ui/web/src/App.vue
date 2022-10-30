<template>
  <ProgressBar></ProgressBar>
  <div class="container">
    <RouterView />
  </div>
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import { ProgressBar } from "@marcoschulte/vue3-progress"

export default defineComponent({
  name: "App",
  components: { RouterView, ProgressBar },
})
</script>

<style>
.vue3-progress-bar-container .vue3-progress-bar {
  background-color: hsl(217, 71%, 53%) !important;
}
</style>
