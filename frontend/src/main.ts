import { createApp } from "vue"
import { createPinia } from "pinia"
import { Vue3ProgressPlugin } from "@marcoschulte/vue3-progress"
import Toast from "vue-toastification"
import App from "./App.vue"
import router from "@/router/index"

import "vue-select/dist/vue-select.css"
import "@marcoschulte/vue3-progress/dist/index.css"
import "vue-toastification/dist/index.css"

console.info("App version", import.meta.env.VITE_APP_VERSION)

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Vue3ProgressPlugin)
app.use(Toast, {
  transition: "Vue-Toastification__fade",
  maxToasts: 4,
  draggable: false,
  hideProgressBar: true,
})

app.mount("#app")
