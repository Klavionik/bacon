<template>
  <img :src="oval" alt="loading" :width="width" :height="height" />
</template>

<script lang="ts">
import oval from "@/assets/oval.svg"
import { defineComponent } from "vue"

export default defineComponent({
  name: "AppLoader",
  props: {
    width: {
      type: String,
      default: "50",
    },
    height: {
      type: String,
      default: "50",
    },
  },
  data() {
    return {
      oval,
    }
  },
})
</script>
