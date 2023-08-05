export type UserMeta = {
  telegramId?: number
  telegramNotifications?: boolean
}

export type UserCreate = {
  email: string
  password: string
  repeatPassword: string
}

export type UserCreateServer = {
  email: string
  password: string
  re_password: string
}

export type UserRead = {
  id: number
  email: string
  meta: UserMeta
}

export type UserLogin = {
  email: string
  password: string
}

export type UserToken = {
  access_token: string
}

export type UserUpdate = {
  email?: string
  password?: string
  meta?: UserMeta
}
