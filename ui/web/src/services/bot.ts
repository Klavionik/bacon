import ky from "ky"
import type { KyInstance } from "ky/distribution/types/ky"
import type { DeepLink } from "@/models/bot"

class BotService {
  public client: KyInstance

  constructor(baseUrl: string, prefix: string) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({
      prefixUrl,
      timeout: 15000,
    })
  }

  getDeepLink(): Promise<DeepLink> {
    return this.client.get("deep_link").json()
  }

  setToken(token: string) {
    this.client = this.client.extend({
      headers: { authorization: `Bearer ${token}` },
    })
  }
}

export default new BotService(import.meta.env.VITE_API_URL, "bot")
