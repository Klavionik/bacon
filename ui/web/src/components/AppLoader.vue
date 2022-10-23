<template>
  <img :src="oval" alt="loading" :width="width" :height="height" />
</template>

<script>
import oval from "@/assets/oval.svg"

export default {
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
}
</script>
