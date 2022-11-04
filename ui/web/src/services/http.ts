import type { KyInstance } from "ky/distribution/types/ky"
import ky from "ky"

export class BaseHTTPService {
  public client: KyInstance

  constructor(baseUrl: string, prefix: string) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({
      prefixUrl,
      timeout: 15000,
    })
  }

  setToken(token: string) {
    this.client = this.client.extend({
      headers: { authorization: `Bearer ${token}` },
    })
  }

  removeToken() {
    this.client.extend({ headers: { authorization: undefined } })
  }
}
