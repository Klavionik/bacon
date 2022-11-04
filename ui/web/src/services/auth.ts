import type { UserCreate, UserLogin, UserRead, UserToken, UserUpdate } from "@/models/user"
import { BaseHTTPService } from "@/services/http"

class AuthService extends BaseHTTPService {
  async signup(user: UserCreate): Promise<UserRead> {
    const response = await this._post("register", { json: user })
    return response.json()
  }

  async login(user: UserLogin): Promise<UserToken> {
    const formData = new FormData()
    formData.append("username", user.email)
    formData.append("password", user.password)
    const response = await this._post("login", { body: formData })
    return response.json()
  }

  async getMe(): Promise<UserRead> {
    const response = await this._get("me")
    return response.json()
  }

  async updateMe(user: UserUpdate): Promise<UserRead> {
    const response = await this._patch("me", { json: user })
    return response.json()
  }
}

export default new AuthService(import.meta.env.VITE_API_URL, "auth")
