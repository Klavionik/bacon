<template>
  <section class="section" :class="{ 'p-0': isMobile }">
    <div class="container"><slot></slot></div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useIsMobile } from "@/utils"

export default defineComponent({
  name: "AppSection",
  data() {
    return {
      isMobile: useIsMobile(),
    }
  },
})
</script>
