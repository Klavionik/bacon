<template>
  <nav class="navbar is-light">
    <div class="navbar-brand">
      <RouterLink class="navbar-item" to="/">
        <img src="/logo.jpg" alt="Treats" />
      </RouterLink>
      <RouterLink class="navbar-item" :to="{ name: 'treats' }"> Мои вкусняшки </RouterLink>
    </div>
    <div class="navbar-menu is-active">
      <div class="navbar-start" />
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <RouterLink class="button is-light" :to="{ name: 'profile' }">
              <i class="fa-sharp fa-solid fa-gear" />
            </RouterLink>
            <a class="button is-light" @click="() => {}">
              <i class="fa-sharp fa-solid fa-arrow-right-from-bracket" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "NavBar",
})
</script>
