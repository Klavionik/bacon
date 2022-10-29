export const enum LoginFormMode {
  LOGIN = "login",
  SIGNUP = "signup",
}

export const validFormModes = [LoginFormMode.LOGIN, LoginFormMode.SIGNUP]

export type TabRecord = {
  title: string
  id: string
}

export const settingsTabs: Array<TabRecord> = [
  { title: "Профиль", id: "profile" },
  { title: "Магазины", id: "shops" },
  { title: "Уведомления", id: "notifications" },
]
