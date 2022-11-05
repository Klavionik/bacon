import type { Options } from "ky"

export type RequestOptions = [url: string, options?: Options]

export interface HTTPClient {
  [n: string]: any
  baseURL: string
  get(...args: RequestOptions): Promise<any>
  post(...args: RequestOptions): Promise<any>
  put(...args: RequestOptions): Promise<any>
  patch(...args: RequestOptions): Promise<any>
  delete(...args: RequestOptions): Promise<any>
}

export interface HTTPService {
  readonly client: HTTPClient
  readonly prefix: string
}
