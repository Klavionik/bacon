<template>
  <form class="form">
    <div class="field">
      <span class="icon-text">
        <span class="icon">
          <i class="fa-brands fa-telegram" :class="[telegramEnabled ? 'has-text-link' : '']"></i>
        </span>
        <span :class="[telegramEnabled ? 'has-text-link' : '']">Telegram</span>
      </span>
      <div class="help">
        <template v-if="telegramEnabled"
          >Вы получаете уведомления в Telegram.
          <a href="" @click.prevent="disableTelegram">Отключить уведомления</a></template
        >
        <template v-else
          >Чтобы получать уведомления об изменении цены и доступности товаров от Telegram-бота,
          <a :href="botDeepLink" target="_blank"
            >перейдите по этой ссылке и отправьте сообщение боту.</a
          >
        </template>
      </div>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useUserStore } from "@/stores/user"
import { mapWritableState } from "pinia"
import { services } from "@/http"

export default defineComponent({
  name: "UserNotifications",
  data() {
    return {
      botDeepLink: "",
    }
  },
  computed: {
    ...mapWritableState(useUserStore, ["user"]),
    telegramEnabled(): boolean {
      return Boolean(this.user.meta.telegramNotifications)
    },
  },
  async mounted() {
    if (!this.telegramEnabled) {
      const data = await services.getDeepLink()
      this.botDeepLink = data.link
    }
  },
  methods: {
    async disableTelegram() {
      const payload = { meta: { telegramNotifications: false } }
      this.user = await services.updateMe(payload)
    },
  },
})
</script>

<style scoped></style>
