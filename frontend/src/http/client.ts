import type { KyInstance } from "ky/distribution/types/ky"
import ky from "ky"
import { request } from "./decorators"
import type { HTTPClient, RequestOptions } from "@/http/types"

export class Client implements HTTPClient {
  private client: KyInstance
  public baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
    this.client = ky.create({
      prefixUrl: baseURL,
      timeout: 15000,
    })
  }

  @request()
  get(...args: RequestOptions) {
    return this.client.get(...args)
  }

  @request()
  post(...args: RequestOptions) {
    return this.client.post(...args)
  }

  @request()
  put(...args: RequestOptions) {
    return this.client.put(...args)
  }

  @request()
  patch(...args: RequestOptions) {
    return this.client.patch(...args)
  }

  @request()
  delete(...args: RequestOptions) {
    return this.client.delete(...args)
  }

  setToken(token: string) {
    this.client = this.client.extend({
      headers: { authorization: `JWT ${token}` },
    })
  }

  removeToken() {
    this.client.extend({ headers: { authorization: undefined } })
  }
}
