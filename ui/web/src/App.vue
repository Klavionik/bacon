<template>
  <ProgressBar></ProgressBar>
  <RouterView />
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import { ProgressBar } from "@marcoschulte/vue3-progress"
import { Unauthorized } from "@/http/errors"
import { useToast } from "vue-toastification"
import { useUserStore } from "@/stores/user"

export default defineComponent({
  name: "App",
  components: { RouterView, ProgressBar },
  setup() {
    const { logout } = useUserStore()
    const toast = useToast()
    return { logout, toast }
  },
  errorCaptured(err) {
    if (err instanceof Unauthorized) {
      this.toast.warning("Время сессии истекло. Войдите заново.")
      this.logout()
      this.$router.push("/")
      return false
    }
  },
})
</script>

<style>
.vue3-progress-bar-container .vue3-progress-bar {
  background-color: hsl(217, 71%, 53%) !important;
}

body {
  font-family: "Rubik", sans-serif;
}

@font-face {
  font-family: "Rubik";
  font-weight: 400;
  src: url("@/assets/Rubik-Regular.ttf") format("truetype");
}

@font-face {
  font-family: "Rubik";
  font-weight: 500;
  src: url("@/assets/Rubik-SemiBold.ttf") format("truetype");
}

@font-face {
  font-family: "Rubik";
  font-weight: 400;
  font-style: italic;
  src: url("@/assets/Rubik-Italic.ttf") format("truetype");
}
</style>
