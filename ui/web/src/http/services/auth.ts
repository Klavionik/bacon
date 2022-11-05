import type { UserCreate, UserLogin, UserRead, UserToken, UserUpdate } from "@/models/user"
import client from "@/http/client"
import type { HTTPService, HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

class AuthService implements HTTPService {
  client
  prefix = "auth/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async signup(user: UserCreate): Promise<UserRead> {
    const response = await this.client.post("register", { json: user })
    return response.json()
  }

  async login(user: UserLogin): Promise<UserToken> {
    const formData = new FormData()
    formData.append("username", user.email)
    formData.append("password", user.password)
    const response = await this.client.post("login", { body: formData })
    return response.json()
  }

  async getMe(): Promise<UserRead> {
    const response = await this.client.get("me")
    return response.json()
  }

  async updateMe(user: UserUpdate): Promise<UserRead> {
    const response = await this.client.patch("me", { json: user })
    return response.json()
  }
}

export default new AuthService(client)
