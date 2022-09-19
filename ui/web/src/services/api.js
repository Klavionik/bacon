import ky from 'ky'

class APIService {
  constructor(baseUrl, prefix, token) {
    const prefixUrl = String(new URL(prefix, baseUrl))
    this.client = ky.create({
      prefixUrl,
      headers: { 'Authorization': `Token ${token}`},
      timeout: 15000
    })
  }

  listShops() {
    return this.client.get('shops')
  }

  listUserTreats() {
    return this.client.get('treats/user')
  }

  createTreat(url) {
    return this.client.post('treats', {json: {url}})
  }

  deleteTreat(id) {
    return this.client.delete(`treats/${id}`)
  }
}

export default APIService
