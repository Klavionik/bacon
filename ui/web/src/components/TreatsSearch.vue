<template>
  <div class="panel-block">
    <p class="control has-icons-left">
      <input :value="search" class="input" type="text" placeholder="Поиск" @input="emitSearch" />
      <span class="icon is-left"><i class="fas fa-search" /></span>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "TreatsSearch",
  props: {
    search: {
      type: String,
      required: true,
    },
  },
  emits: ["update:search"],
  methods: {
    emitSearch(event: Event) {
      const target = event.target as HTMLInputElement
      this.$emit("update:search", target.value)
    },
  },
})
</script>
