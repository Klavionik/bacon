import { createApp } from "vue"
import { createPinia } from "pinia"
import { createAuth0 } from "@auth0/auth0-vue"

import App from "./App.vue"
import router from "@/router/index"

import "vue-select/dist/vue-select.css"

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(
  createAuth0({
    domain: "treats.eu.auth0.com",
    client_id: "rY17YOsld4TM7l7kE0Ycv8vr0l0nPTg4",
    redirect_uri: "http://localhost:5173/app/",
    audience: "https://treats.klavionik.me",
  })
)

app.mount("#app")
