import type { DeepLink } from "@/models/bot"
import type { HTTPService } from "@/http/services/types"
import type { HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

export class BotService implements HTTPService {
  client
  prefix = "api/notifications/v1/telegram/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async checkSubscription() {
    const response = await this.client.get("subscription/")
    return response.status !== 204
  }

  async deleteSubscription() {
    return await this.client.delete("subscription/")
  }

  async getDeepLink(): Promise<DeepLink> {
    const response = await this.client.get("deep_link/")
    return response.json()
  }
}
