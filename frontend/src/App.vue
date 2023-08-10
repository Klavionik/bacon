<template>
  <ProgressBar></ProgressBar>
  <RouterView />
</template>

<script lang="ts">
import { RouterView } from "vue-router"
import { defineComponent } from "vue"
import { ProgressBar } from "@marcoschulte/vue3-progress"
import { TokenExpired } from "@/http/errors"
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
    if (err instanceof TokenExpired) {
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

html,
body {
  font-family: "Rubik", sans-serif;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}

#app > main {
  flex: 1 0 auto;
}

#app > .footer {
  flex-shrink: 0;
}

#app > nav {
  flex-shrink: 0;
}

.no-shadow {
  box-shadow: none;
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
