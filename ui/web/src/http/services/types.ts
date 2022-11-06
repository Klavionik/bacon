import type { APIService } from "@/http/services/api"
import type { AuthService } from "@/http/services/auth"
import type { BotService } from "@/http/services/bot"
import type { HTTPClient } from "@/http/types"

interface HTTPService {
  [n: string]: any
  readonly client: HTTPClient
  readonly prefix: string
}

type EveryService = APIService & AuthService & BotService
type ServiceMethods = Omit<EveryService, "client" | "prefix">

export type { HTTPService, ServiceMethods }
