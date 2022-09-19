class TelegramService {
  get telegram() {
    return window.Telegram.WebApp
  }

  get initData() {
    return this.telegram.initDataUnsafe
  }

  ready() {
    return this.telegram.ready()
  }

  expand() {
    return this.telegram.expand()
  }
}

const telegramService = new TelegramService()

export default telegramService
