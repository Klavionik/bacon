import type { HTTPService, ServiceMethods } from "@/http/services/types"
import type { HTTPClient } from "@/http"
import { APIService } from "@/http/services/api"
import { AuthService } from "@/http/services/auth"
import { BotService } from "@/http/services/bot"

const services = [APIService, AuthService, BotService]

const createServicesHandler = (serviceInstances: HTTPService[]) => {
  return {
    get(target: ServiceMethods, p: string): any {
      for (const service of serviceInstances) {
        const method = service[p]
        if (method) return method.bind(service)
      }

      throw Error(`Method ${p} does not exist in any service.`)
    },
  }
}

const createServices = (obj: ServiceMethods, client: HTTPClient): ServiceMethods => {
  const serviceInstances = services.map((serviceConstuctor) => new serviceConstuctor(client))
  return new Proxy(obj, createServicesHandler(serviceInstances))
}

export { createServices }
