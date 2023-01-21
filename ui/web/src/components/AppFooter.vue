<template>
  <footer class="footer">
    <p class="has-text-centered">
      Автор проекта
      <span class="icon-text">
        <span class="icon mr-0">
          <i class="fa-brands fa-github"></i>
        </span>
        <a href="https://github.com/Klavionik">Klavionik</a>
      </span>
    </p>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "AppFooter",
})
</script>

<style scoped>
.footer {
  padding: 1rem 1.5rem 2rem;
}
</style>
