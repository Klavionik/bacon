class Unauthorized extends Error {}
class BadRequest extends Error {
  public detail: string

  constructor(message: string, detail: string, options?: object) {
    // @ts-ignore
    super(message, options)
    this.detail = detail
  }
}

export { Unauthorized, BadRequest }
