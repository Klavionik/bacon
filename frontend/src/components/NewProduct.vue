<template>
  <div class="panel-block">
    <div class="field has-addons width-100">
      <p class="control is-flex-grow-1 has-icons-left">
        <input
          :value="url"
          class="input"
          :disabled="noShopLocationsConfigured"
          type="text"
          placeholder="Добавить"
          @input="emitURL"
        />
        <span class="icon is-left"><i class="fas fa-link" /></span>
      </p>
      <p class="control">
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
import { mapStores } from "pinia"
import { useShopsStore } from "@/stores/shop"
import { useShopLocationsStore } from "@/stores/shop-location"

export default defineComponent({
  name: "NewProduct",
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
  computed: {
    ...mapStores(useShopsStore, useShopLocationsStore),
    isValidURL() {
      const shop = this.shopStore.getShopByProductURL(this.url)

      if (!shop) return false

      return this.shopLocationStore.isShopLocationConfigured(shop.id)
    },
    noShopLocationsConfigured() {
      return this.shopLocationStore.noShopLocationsConfigured
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
