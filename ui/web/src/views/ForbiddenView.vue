<template>
  <div class="box is-flex is-flex-direction-column is-flex-align-items-center p-5 m-5">
    <i class="fa-solid fa-ban fa-2xl mx-auto has-text-danger mb-2">&nbsp;403</i>
    <p class="mt-5">Простите, у вас нет доступа к этому приложению. :(</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "ForbiddenView",
})
</script>
