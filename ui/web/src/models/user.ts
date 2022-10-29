export type UserCreate = {
  email: string
  password: string
  repeatPassword: string
}

export type UserRead = {
  id: number
  email: string
}

export type UserLogin = {
  email: string
  password: string
}

export type UserToken = {
  access_token: string
}
