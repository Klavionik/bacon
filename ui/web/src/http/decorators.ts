import { handleError } from "@/http/utils"
import type { RequestOptions } from "@/http/types"

export const request = () => {
  return (target: any, key: string, descriptor: PropertyDescriptor) => {
    const func = descriptor.value
    descriptor.value = function (...args: RequestOptions) {
      return func.apply(this, args).catch(handleError)
    }

    return descriptor
  }
}
