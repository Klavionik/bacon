import App from "./App.svelte"
import telegramService from "./services/telegram.js"

// telegramService.ready()
// telegramService.expand()
const initData = {"query_id": "AAG5caYEAAAAALlxpgTDGeXU", "user": {"id": 78016953, "first_name": "Roman", "last_name": "Vlasenko", "username": "Jediroman", "language_code": "ru"}, "auth_date": "1662909304", "hash": "ae2883de3c73b6cd51d8ad92f2c01f0d91e213386b88519c0af6b83d00449d1d"}
const app = new App({
  target: document.getElementById("app"),
  props: {
    initData
  }
})

export default app
