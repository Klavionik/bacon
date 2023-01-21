<template>
  <NavBar />
  <section class="hero is-medium">
    <div class="hero-body">
      <p class="title">Вкусняшки</p>
      <p class="subtitle has-text-danger">Пора купить!</p>
    </div>
  </section>
  <section class="section">
    <p class="has-text-left">
      С помощью приложения <span class="has-text-weight-semibold">Вкусняшек</span> можно отслеживать
      ваши любимые товары и получать уведомления об изменении цены и наличия в магазине.
    </p>
  </section>
  <section class="section container">
    <div class="columns">
      <div class="column has-text-centered">
        <p class="title">Бесплатно</p>
        <p>Никакой платной подписки или премиум-аккаунтов.</p>
      </div>
      <div class="column has-text-centered">
        <p class="title">Просто</p>
        <p>
          Регистрация и настройка аккаунта займет
          <span class="has-text-weight-semibold">1 минуту</span>.
        </p>
      </div>
      <div class="column has-text-centered">
        <p class="title">Удобно</p>
        <p>Управляйте списком отслеживания с телефона, планшета или компьютера.</p>
      </div>
    </div>
  </section>
  <section class="footer">
    <p class="has-text-centered">
      Автор проекта
      <span class="icon-text">
        <span class="icon mr-0">
          <i class="fa-brands fa-github"></i>
        </span>
        <a href="https://github.com/Klavionik">Klavionik</a>
      </span>
    </p>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "@/components/NavBar.vue"

export default defineComponent({
  name: "HomeView",
  components: { NavBar },
})
</script>

<style scoped></style>
