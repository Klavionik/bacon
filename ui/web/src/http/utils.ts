import { useToast } from "vue-toastification"
import { HTTPError, TimeoutError } from "ky"
import { Unauthorized, BadRequest } from "@/http/errors"
import type { HTTPService, HTTPClient, RequestOptions } from "@/http/types"

const toast = useToast()
const proxiedMethods: string[] = ["get", "post", "put", "patch", "delete"]

const isProxiedMethod = (prop: string) => {
  return proxiedMethods.includes(prop)
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

const clientServiceProxy = (client: HTTPClient, service: HTTPService): HTTPClient => {
  return new Proxy(client, {
    get(client: HTTPClient, property: string): any {
      if (!isProxiedMethod(property)) return Reflect.get(client, property)

      return new Proxy(client[property], {
        apply(method: any, thisArg: object, argArray: RequestOptions): any {
          /*
              Build endpoint URL.
              Example:
                baseURL = http://localhost/
                prefix = "api/"
                argArray[0] = "shops"
              Result: "http://localhost/api/shops"
             */
          let url = new URL(service.prefix, client.baseURL)
          url = new URL(argArray[0], url)
          return method.bind(client)(url, argArray[1])
        },
      })
    },
  })
}

export { handleError, clientServiceProxy }
