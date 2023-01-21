<template>
  <div class="columns is-centered">
    <div class="column is-two-fifths">
      <div class="section mx-auto">
        <div class="card">
          <div class="card-content">
            <div class="p-5">
              <h1 class="is-size-4 has-text-centered">Добро пожаловать!</h1>
              <h1 class="is-size-7 has-text-centered">Вкусняшки уже ждут</h1>
              <div class="mt-5">
                <div class="tabs is-centered is-toggle">
                  <ul>
                    <li :class="{ 'is-active': !signupTabActive }" @click="activateLoginTab">
                      <a>Вход</a>
                    </li>
                    <li :class="{ 'is-active': signupTabActive }" @click="activateSignupTab">
                      <a>Регистрация</a>
                    </li>
                  </ul>
                </div>
                <LoginForm :mode="activeTab" @submit:login="login" @submit:signup="signup" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import LoginForm from "@/components/LoginForm.vue"
import { LoginFormMode } from "@/consts"
import { useUserStore } from "@/stores/user"
import type { UserCreate } from "@/models/user"
import { mapStores } from "pinia"

export default defineComponent({
  name: "LoginView",
  components: { LoginForm },
  data() {
    return {
      activeTab: LoginFormMode.LOGIN as LoginFormMode,
    }
  },
  computed: {
    ...mapStores(useUserStore),
    signupTabActive() {
      return this.activeTab === LoginFormMode.SIGNUP
    },
  },
  methods: {
    activateLoginTab() {
      this.activeTab = LoginFormMode.LOGIN
    },
    activateSignupTab() {
      this.activeTab = LoginFormMode.SIGNUP
    },
    async login(payload: UserCreate) {
      await this.userStore.login(payload)

      if (this.userStore.loggedIn) {
        this.redirectNext()
      }
    },
    async signup(payload: UserCreate) {
      await this.userStore.signup(payload)

      if (this.userStore.loggedIn) {
        this.$router.push("/")
      }
    },
    redirectNext() {
      const { next } = this.$route.query

      if (next) return this.$router.push(next as string)
      this.$router.push("/")
    },
  },
})
</script>
