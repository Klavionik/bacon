import { useBreakpoints as _useBreakpoints } from "@vueuse/core"
import { breakpointsBulma } from "@/consts"

export function useBreakpoints() {
  return _useBreakpoints(breakpointsBulma)
}

export function useIsMobile() {
  const breakpoints = useBreakpoints()
  return breakpoints.smaller("desktop")
}
