import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "@/router/index"

import "vue-select/dist/vue-select.css"

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount("#app")
