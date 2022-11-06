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
</style>
