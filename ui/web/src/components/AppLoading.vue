<template>
  <div class="preloader">
    <AppLoader class="load" width="100" height="100" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import AppLoader from "./AppLoader.vue"

export default defineComponent({
  name: "AppPreloader",
  components: { AppLoader },
})
</script>

<style scoped>
.preloader {
  height: 100vh;
  width: 100vw;
}

.load {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
