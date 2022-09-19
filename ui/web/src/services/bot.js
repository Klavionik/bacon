import ky from 'ky'

class BotService {
  constructor(baseUrl, prefix) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({prefixUrl})
  }

  start(initData) {
    return this.client.post('start', {json: initData})
  }
}

const botService = new BotService(import.meta.env.TREATS_SERVER_URL, '/bot/')

export default botService
