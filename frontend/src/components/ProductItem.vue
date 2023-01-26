<template>
  <article class="panel-block" :class="{ 'is-disabled': isDeleting || !product.available }">
    <div class="media is-flex-grow-1">
      <div class="media-content pl-3">
        <div class="content">
          <div>
            <strong>{{ product.title }}</strong>
            <span class="mx-2">
              <a class="tag mx-1 is-light is-info" :href="product.url">{{ product.shopTitle }}</a>
              <span v-if="!product.available" class="tag mx-1 is-light is-warning"
                >Нет в наличии</span
              >
            </span>
            <br />
            <span
              >Цена: <del v-if="discounted">{{ product.oldPrice }} &#8381;</del>
              {{ product.price }} &#8381;
            </span>
          </div>
        </div>
      </div>
      <div class="my-auto">
        <button
          class="button is-inverted is-outlined is-danger"
          :class="{ 'is-loading': isDeleting }"
          @click="$emit('delete', product.id)"
        >
          <span class="icon" :class="{ 'is-invisible': isDeleting }"
            ><i class="delete has-background-danger"
          /></span>
        </button>
      </div>
    </div>
  </article>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import type { PropType } from "vue"
import type { Product } from "@/models/product"

export default defineComponent({
  name: "ProductItem",
  props: {
    product: {
      type: Object as PropType<Product>,
      required: true,
    },
    isDeleting: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["delete"],
  computed: {
    discounted(): boolean {
      return this.product.oldPrice !== null && this.product.price < this.product.oldPrice
    },
  },
})
</script>

<style scoped>
.is-disabled {
  opacity: 0.5;
}
</style>
