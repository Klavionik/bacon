import { useBreakpoints as _useBreakpoints } from "@vueuse/core"
import { breakpointsBulma } from "@/consts"
import { decodeJwt } from "jose"

const JWT_LEEWAY_SECONDS = 10 * 1000

export function useBreakpoints() {
  return _useBreakpoints(breakpointsBulma)
}

export function useIsMobile() {
  const breakpoints = useBreakpoints()
  return breakpoints.smaller("desktop")
}

export function isJWTExpired(token: string): boolean {
  const payload = decodeJwt(token)
  const expiresAt = payload.exp! * 1000 - JWT_LEEWAY_SECONDS
  return Date.now() > expiresAt
}
