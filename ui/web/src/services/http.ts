import type { KyInstance } from "ky/distribution/types/ky"
import ky, { HTTPError, type Options, TimeoutError } from "ky"
import { useToast } from "vue-toastification"

type RequestOptions = [url: string, options?: Options]

export class Unauthorized extends Error {}
export class BadRequest extends Error {
  public detail: string

  constructor(message: string, detail: string, options?: object) {
    // @ts-ignore
    super(message, options)
    this.detail = detail
  }
}

const toast = useToast()

const request = () => {
  return (target: any, key: string, descriptor: PropertyDescriptor) => {
    const func = descriptor.value
    descriptor.value = function (...args: RequestOptions) {
      return func.apply(this, args).catch(handleError)
    }

    return descriptor
  }
}

const handleError = async (e: any) => {
  if (e instanceof HTTPError) {
    await handleHTTPError(e)
  }

  if (e instanceof TimeoutError) {
    toast.error("Не удалось выполнить запрос. Проверьте подключение к интернету.")
  }

  throw e
}

const handleHTTPError = async (e: HTTPError) => {
  if (e.response.status === 401) {
    throw new Unauthorized("Unauthorized")
  }

  if (e.response.status === 400) {
    const { detail } = await e.response.json()
    throw new BadRequest("Bad Request", detail)
  }

  throw e
}

export class BaseHTTPService {
  public client: KyInstance

  constructor(baseUrl: string, prefix: string) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({
      prefixUrl,
      timeout: 15000,
    })
  }

  @request()
  _get(...args: RequestOptions) {
    return this.client.get(...args)
  }

  @request()
  _post(...args: RequestOptions) {
    return this.client.post(...args)
  }

  @request()
  _put(...args: RequestOptions) {
    return this.client.put(...args)
  }

  @request()
  _patch(...args: RequestOptions) {
    return this.client.patch(...args)
  }

  @request()
  _delete(...args: RequestOptions) {
    return this.client.delete(...args)
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
