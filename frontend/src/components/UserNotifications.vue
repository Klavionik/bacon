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

interface ComponentData {
  telegramEnabled: boolean
  botDeepLink: string
}

export default defineComponent({
  name: "UserNotifications",
  async beforeRouteEnter(to, from, next) {
    const telegramEnabled = await services.checkSubscription()
    let botDeepLink = ""

    if (!telegramEnabled) {
      botDeepLink = (await services.getDeepLink()).link
    }

    next((component) => {
      const data = component.$data as ComponentData
      data.telegramEnabled = telegramEnabled
      data.botDeepLink = botDeepLink
    })
  },
  data(): ComponentData {
    return {
      botDeepLink: "",
      telegramEnabled: false,
    }
  },
  computed: {
    ...mapWritableState(useUserStore, ["user"]),
  },
  methods: {
    async disableTelegram() {
      await services.deleteSubscription()
      this.telegramEnabled = false
      this.botDeepLink = (await services.getDeepLink()).link
    },
  },
})
</script>

<style scoped></style>
