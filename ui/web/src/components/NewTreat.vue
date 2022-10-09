<template>
  <div class="panel-block">
    <div class="is-flex width-100">
      <p class="control is-flex-grow-1">
        <input :value="url" class="input" type="text" placeholder="Ссылка" @input="emitURL" />
      </p>
      <p class="control ml-1">
        <button
          :disabled="!isValidURL"
          class="button"
          :class="{ 'is-loading': isLoading }"
          type="submit"
          @click="$emit('submit')"
        >
          <span class="icon is-left" :class="{ 'is-invisible': isLoading }"
            ><i class="fas fa-circle-plus has-text-primary"
          /></span>
        </button>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useShopsStore } from "@/stores/shops"

export default defineComponent({
  name: "NewTreat",
  props: {
    url: {
      type: String,
      required: true,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["submit", "update:url"],
  setup() {
    const shopsStore = useShopsStore()
    return { shopsStore }
  },
  computed: {
    isValidURL() {
      return this.shopsStore.shopUrlRules.some((rule) => rule.test(this.url))
    },
  },
  methods: {
    emitURL(event: Event) {
      const target = event.target as HTMLInputElement
      this.$emit("update:url", target.value)
    },
  },
})
</script>

<style scoped>
.width-100 {
  width: 100%;
}
</style>
