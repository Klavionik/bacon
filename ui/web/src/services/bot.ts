import type { DeepLink } from "@/models/bot"
import { BaseHTTPService } from "@/services/http"

class BotService extends BaseHTTPService {
  getDeepLink(): Promise<DeepLink> {
    return this.client.get("deep_link").json()
  }
}

export default new BotService(import.meta.env.VITE_API_URL, "bot")
