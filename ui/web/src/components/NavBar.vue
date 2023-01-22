<template>
  <nav class="navbar has-shadow">
    <div class="container">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          <img class="treats-logo" src="@/assets/logo.svg" alt="Treats" />
        </a>
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
                <a class="navbar-item" href="#">Выйти</a>
              </div>
            </div>
          </template>
          <template v-else>
            <RouterLink class="navbar-item" :to="{ name: 'profile' }">Настройки</RouterLink>
            <a class="navbar-item" href="#">Помощь</a>
            <a class="navbar-item" href="#" @click="logout">Выйти</a>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { mapStores } from "pinia"
import { useUserStore } from "@/stores/user"
import UserEmail from "@/components/UserEmail.vue"

export default defineComponent({
  name: "NavBar",
  components: { UserEmail },
  data() {
    return {
      isHamburgerOpen: false,
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
  methods: {
    logout() {
      this.userStore.logout()
      this.$router.push("/")
    },
  },
})
</script>

<style scoped>
.treats-logo {
  height: 30px;
}

.navbar-menu.is-active {
  position: absolute;
  width: 100%;
}
</style>
