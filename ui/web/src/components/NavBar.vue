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
        <RouterLink v-if="loggedIn" class="navbar-item" :to="{ name: 'treats' }">
          Мои вкусняшки
        </RouterLink>
      </div>
      <div class="navbar-end">
        <div v-if="!loggedIn" class="navbar-item">
          <RouterLink is="button" class="button" :to="{ name: 'login' }">Войти</RouterLink>
        </div>
        <template v-else-if="loggedIn && !isHamburgerOpen">
          <div class="navbar-item mx-3">{{ email }}</div>
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
import { mapStores } from "pinia"
import { useUserStore } from "@/stores/user"

export default defineComponent({
  name: "NavBar",
  data() {
    return {
      isHamburgerOpen: false,
    }
  },
  computed: {
    ...mapStores(useUserStore),
    email() {
      return this.userStore.user.email
    },
    loggedIn() {
      return this.userStore.loggedIn
    },
  },
  methods: {
    logout() {
      this.userStore.logout()
      this.$router.push("/")
    },
  },
})
</script>
