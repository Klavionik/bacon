<template>
  <footer class="footer">
    <p class="has-text-centered">
      Исходный код проекта доступен на
      <span class="icon-text">
        <span class="icon mr-0">
          <i class="fa-brands fa-github"></i>
        </span>
        <a href="https://github.com/Klavionik/bacon">GitHub</a>
      </span>
    </p>
    <p class="has-text-centered">
      Автор баннера
      <a
        href="https://www.freepik.com/free-vector/bacon-pattern-food-wallpaper-illustration_3450207.htm"
        >rawpixel.com</a
      >
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
