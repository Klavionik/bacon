<template>
  <div class="navbar-item mx-3">
    <span class="icon-text">
      <span class="icon mr-0"><i class="fa-solid fa-user"></i></span>
      <span class="text">
        <slot></slot>
      </span>
    </span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "UserEmail",
})
</script>

<style scoped>
.text {
  cursor: default;
}
</style>
