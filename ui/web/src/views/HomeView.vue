<template>
  <section class="hero is-medium is-relative">
    <div class="image"></div>
    <div class="hero-body">
      <div class="container">
        <div class="columns">
          <div class="column is-two-fifths">
            <p class="title has-text-white">Вкусняшки</p>
            <p class="subtitle has-text-white">
              Отслеживайте ваши любимые товары и получайте уведомления об изменении цены и наличия в
              магазине.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
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
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "HomeView",
})
</script>

<style scoped>
.image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/hero.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  filter: brightness(0.75);
}
</style>
