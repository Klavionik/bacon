class APIError extends Error {
  public detail?: string

  constructor(message: string, detail?: string, options?: object) {
    // @ts-ignore
    super(message, options)
    this.detail = detail
  }
}

class Unauthorized extends APIError {}

class BadRequest extends APIError {}

class Conflict extends APIError {}

class TokenExpired extends Error {}

export { Unauthorized, BadRequest, Conflict, TokenExpired }
