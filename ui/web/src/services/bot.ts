import type { DeepLink } from "@/models/bot"
import { BaseHTTPService } from "@/services/http"

class BotService extends BaseHTTPService {
  async getDeepLink(): Promise<DeepLink> {
    const response = await this._get("deep_link")
    return response.json()
  }
}

export default new BotService(import.meta.env.VITE_API_URL, "bot")
