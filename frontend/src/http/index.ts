import { Client } from "@/http/client"
import { createServices } from "@/http/services"
import type { ServiceMethods } from "@/http/services/types"

export const client = new Client(import.meta.env.VITE_API_URL)
export const services = createServices({} as ServiceMethods, client)

export type { HTTPClient } from "./types"
export type { HTTPService } from "./services/types"
