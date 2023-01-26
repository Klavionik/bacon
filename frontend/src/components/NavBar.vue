<template>
  <nav class="navbar has-shadow">
    <div class="container">
      <div ref="navbarBrand" class="navbar-brand">
        <a class="navbar-item" href="/">
          <img class="logo" src="@/assets/logo.svg" alt="Logo" />
        </a>
        <a class="navbar-burger" :class="{ 'is-active': isHamburgerOpen }" @click="toggleHamburger">
          <span></span>
          <span></span>
          <span></span>
        </a>
      </div>
      <div class="navbar-menu" :class="{ 'is-active': isHamburgerOpen }">
        <div class="navbar-start">
          <RouterLink v-if="loggedIn" class="navbar-item" :to="{ name: 'products' }">
            Список товаров
          </RouterLink>
        </div>
        <div class="navbar-end">
          <template v-if="!loggedIn">
            <RouterLink class="navbar-item" :to="{ name: 'login' }">Войти</RouterLink>
          </template>
          <template v-else-if="loggedIn && !isHamburgerOpen">
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link is-arrowless">
                <UserEmail>{{ email }}</UserEmail>
              </a>
              <div class="navbar-dropdown is-boxed">
                <RouterLink class="navbar-item" :to="{ name: 'profile' }">Настройки</RouterLink>
                <a class="navbar-item" href="#">Помощь</a>
                <hr class="navbar-divider" />
                <a class="navbar-item" href="/" @click.prevent="logout">Выйти</a>
              </div>
            </div>
          </template>
          <template v-else>
            <RouterLink class="navbar-item" :to="{ name: 'profile' }">Настройки</RouterLink>
            <a class="navbar-item" href="#">Помощь</a>
            <a class="navbar-item" href="/" @click.prevent="logout">Выйти</a>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, type Ref } from "vue"
import { mapStores } from "pinia"
import { useUserStore } from "@/stores/user"
import { onClickOutside } from "@vueuse/core"
import UserEmail from "@/components/UserEmail.vue"
import { noop } from "@vueuse/core"

export default defineComponent({
  name: "NavBar",
  components: { UserEmail },
  data() {
    return {
      isHamburgerOpen: false,
      hamburgerOutsideClickCleanup: noop,
    }
  },
  computed: {
    ...mapStores(useUserStore),
    email(): string {
      return this.userStore.user.email
    },
    loggedIn(): boolean {
      return this.userStore.loggedIn
    },
  },
  mounted() {
    const navbar = this.$refs.navbar as Ref
    onClickOutside(navbar, () => {
      this.isHamburgerOpen = false
    })
  },
  methods: {
    logout() {
      this.userStore.logout()
      this.$router.push("/")
    },
    toggleHamburger() {
      const closeHamburger = () => {
        this.hamburgerOutsideClickCleanup()
        this.isHamburgerOpen = false
      }

      const openHamburger = () => {
        const navbar = this.$refs.navbarBrand as Ref
        this.hamburgerOutsideClickCleanup = onClickOutside(navbar, closeHamburger) || noop
        this.isHamburgerOpen = true
      }

      if (this.isHamburgerOpen) {
        closeHamburger()
        return
      }

      openHamburger()
    },
  },
})
</script>

<style scoped>
.logo {
  height: 30px;
}

.navbar-menu.is-active {
  position: absolute;
  width: 100%;
}
</style>
