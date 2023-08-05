import type { UserCreateServer, UserLogin, UserRead, UserToken, UserUpdate } from "@/models/user"
import type { HTTPService } from "@/http/services/types"
import type { HTTPClient } from "@/http/types"
import { clientServiceProxy } from "@/http/utils"

export class AuthService implements HTTPService {
  client
  prefix = "auth/"

  constructor(client: HTTPClient) {
    this.client = clientServiceProxy(client, this)
  }

  async signup(user: UserCreateServer): Promise<UserRead> {
    const response = await this.client.post("users/", { json: user })
    return response.json()
  }

  async login(user: UserLogin): Promise<UserToken> {
    const formData = new FormData()
    formData.append("email", user.email)
    formData.append("password", user.password)
    const response = await this.client.post("jwt/create/", { body: formData })
    return response.json()
  }

  async getMe(): Promise<UserRead> {
    const response = await this.client.get("users/me/")
    return response.json()
  }

  async updateMe(user: UserUpdate): Promise<UserRead> {
    const response = await this.client.patch("users/me/", { json: user })
    return response.json()
  }
}
