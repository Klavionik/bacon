import ky from "ky"
import type { KyInstance } from "ky/distribution/types/ky"
import type { UserCreate, UserLogin, UserRead, UserToken } from "@/models/user"

class APIService {
  public client: KyInstance

  constructor(baseUrl: string, prefix: string) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({
      prefixUrl,
      timeout: 15000,
    })
  }

  signup(user: UserCreate): Promise<UserRead> {
    return this.client.post("register", { json: user }).json()
  }

  login(user: UserLogin): Promise<UserToken> {
    const formData = new FormData()
    formData.append("username", user.email)
    formData.append("password", user.password)
    return this.client.post("login", { body: formData }).json()
  }

  getMe(): Promise<UserRead> {
    return this.client.get("me").json()
  }

  setToken(token: string) {
    this.client = this.client.extend({
      headers: { authorization: `Bearer ${token}` },
    })
  }
}

export default new APIService(import.meta.env.VITE_API_URL, "auth")
