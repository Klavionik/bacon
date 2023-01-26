type ApplicationState = {
  accessToken: string
}

type Key = keyof ApplicationState
type Value = ApplicationState[Key]

class AppStorage {
  private _storage = localStorage
  private _appToken = "bacon-v1"

  getItem(key: Key): Value | null {
    const item = this._storage.getItem(this._makeKey(key))
    if (item === null) return item
    return JSON.parse(item)
  }

  setItem(key: Key, value: Value) {
    this._storage.setItem(this._makeKey(key), JSON.stringify(value))
  }

  removeItem(key: Key) {
    this._storage.removeItem(this._makeKey(key))
  }

  _makeKey(key: Key): string {
    return `${this._appToken}-${key}`
  }
}

export default new AppStorage()
