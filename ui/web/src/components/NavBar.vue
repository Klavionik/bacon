<template>
  <nav class="navbar">
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
          <div v-if="!loggedIn" class="navbar-item">
            <RouterLink is="button" class="button" :to="{ name: 'login' }">Войти</RouterLink>
          </div>
          <template v-else-if="loggedIn && !isHamburgerOpen">
            <UserEmail>{{ email }}</UserEmail>
            <div class="navbar-item buttons">
              <RouterLink class="button" :to="{ name: 'profile' }">
                <i class="fa-sharp fa-solid fa-gear fa-lg" />
              </RouterLink>
              <a class="button" @click="logout">
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

.navbar {
  border-bottom: 1px solid #ebeaeb;
}
</style>
