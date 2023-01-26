<template>
  <form @submit.prevent="submit">
    <AppField
      v-model="email"
      name="email"
      :validator="v"
      placeholder="Email"
      :autocomplete="signupMode ? '' : 'username'"
    />
    <AppField
      v-model="password"
      name="password"
      type="password"
      :validator="v"
      placeholder="Пароль"
      :autocomplete="signupMode ? 'new-password' : 'current-password'"
    />
    <AppField
      v-if="signupMode"
      v-model="repeatPassword"
      name="repeatPassword"
      type="password"
      :validator="v"
      placeholder="Повторите пароль"
      autocomplete="new-password"
    />
    <div class="field mt-5">
      <div class="control">
        <button class="button is-link is-fullwidth">
          <template v-if="signupMode">Зарегистрироваться</template>
          <template v-else>Войти</template>
        </button>
      </div>
    </div>
  </form>
</template>

<script lang="ts">
import type { PropType } from "vue"
import { defineComponent } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { minLength, email, sameAs, required, requiredIf } from "@/validators"
import AppField from "@/components/AppField.vue"
import { LoginFormMode, validFormModes } from "@/consts"

export default defineComponent({
  name: "LoginForm",
  components: { AppField },
  props: {
    mode: {
      type: String as PropType<LoginFormMode>,
      default: LoginFormMode.LOGIN,
      validator(value: any) {
        return validFormModes.includes(value)
      },
    },
  },
  emits: ["submit:signup", "submit:login"],
  setup() {
    return { v: useVuelidate() }
  },
  data() {
    return {
      email: "",
      password: "",
      repeatPassword: "",
    }
  },
  computed: {
    signupMode() {
      return this.mode === LoginFormMode.SIGNUP
    },
  },
  validations() {
    return {
      email: { required, email },
      password: { required, minLength: minLength(8) },
      repeatPassword: {
        requiredIf: requiredIf(this.signupMode),
        sameAs: sameAs(this.password),
      },
    }
  },
  watch: {
    mode() {
      this.resetFields()
      this.v.$reset()
    },
  },
  methods: {
    resetFields() {
      this.email = this.password = this.repeatPassword = ""
    },
    async submit() {
      if (!this.signupMode) {
        this.repeatPassword = this.password
      }

      const isFormValid = await this.v.$validate()

      if (!isFormValid) return

      this.$emit(`submit:${this.mode}`, {
        email: this.email,
        password: this.password,
        repeatPassword: this.repeatPassword,
      })
    },
  },
})
</script>
