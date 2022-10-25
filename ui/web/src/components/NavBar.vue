<template>
  <nav class="navbar is-light is-spaced">
    <div class="navbar-brand">
      <RouterLink class="navbar-item" to="/">
        <img src="/logo.jpg" alt="Treats" />
      </RouterLink>
      <a
        class="navbar-burger"
        :class="{ 'is-active': isHamburgerOpen }"
        @click="isHamburgerOpen = !isHamburgerOpen"
      >
        <span></span>
        <span></span>
        <span></span>
      </a>
    </div>
    <div class="navbar-menu" :class="{ 'is-active': isHamburgerOpen }">
      <div class="navbar-start">
        <RouterLink v-if="isAuthenticated" class="navbar-item" :to="{ name: 'treats' }">
          Мои вкусняшки
        </RouterLink>
      </div>
      <div class="navbar-end">
        <div v-if="!isAuthenticated" class="navbar-item">
          <button class="button" @click="login">Войти</button>
        </div>
        <template v-else-if="isAuthenticated && !isHamburgerOpen">
          <div class="navbar-item mx-3">{{ nickname }}</div>
          <div class="navbar-item buttons">
            <RouterLink class="button is-light" :to="{ name: 'profile' }">
              <i class="fa-sharp fa-solid fa-gear fa-lg" />
            </RouterLink>
            <a class="button is-light" @click="logout">
              <i class="fa-sharp fa-solid fa-arrow-right-from-bracket fa-lg" />
            </a>
          </div>
        </template>
        <template v-else>
          <RouterLink class="navbar-item" :to="{ name: 'profile' }">Профиль</RouterLink>
          <a class="navbar-item" href="#" @click="logout">Выйти</a>
        </template>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "NavBar",
  data() {
    return {
      isHamburgerOpen: false,
      user: this.$auth0.idTokenClaims,
      isAuthenticated: this.$auth0.isAuthenticated,
    }
  },
  computed: {
    nickname() {
      return this.user.nickname
    },
  },
  methods: {
    logout() {
      this.$auth0.logout()
    },
    async login() {
      await this.$auth0.loginWithRedirect()
    },
  },
})
</script>
