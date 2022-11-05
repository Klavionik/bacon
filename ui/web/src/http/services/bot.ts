import type { DeepLink } from "@/models/bot"
import client from "@/http/client"
import type { HTTPService, HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

class BotService implements HTTPService {
  client
  prefix = "bot/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async getDeepLink(): Promise<DeepLink> {
    const response = await this.client.get("deep_link")
    return response.json()
  }
}

export default new BotService(client)
