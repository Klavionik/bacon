import type { UserCreate, UserLogin, UserRead, UserToken, UserUpdate } from "@/models/user"
import { BaseHTTPService } from "@/services/http"

class AuthService extends BaseHTTPService {
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

  updateMe(user: UserUpdate): Promise<UserRead> {
    return this.client.patch("me", { json: user }).json()
  }
}

export default new AuthService(import.meta.env.VITE_API_URL, "auth")
