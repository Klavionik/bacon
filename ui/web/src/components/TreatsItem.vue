<template>
  <article class="panel-block" :class="{ 'is-disabled': isDeleting || !treat.available }">
    <div class="media is-flex-grow-1">
      <div class="media-content pl-3">
        <div class="content">
          <div>
            <strong>{{ treat.title }}</strong>
            <span class="mx-2">
              <a class="tag mx-1 is-light is-info" :href="treat.url">{{ treat.shopTitle }}</a>
              <span v-if="!treat.available" class="tag mx-1 is-light is-warning"
                >Нет в наличии</span
              >
            </span>
            <br />
            <span
              >Цена: <del v-if="discounted">{{ treat.oldPrice }} &#8381;</del>
              {{ treat.price }} &#8381;
            </span>
          </div>
        </div>
      </div>
      <div class="my-auto">
        <button
          class="button is-inverted is-outlined is-danger"
          :class="{ 'is-loading': isDeleting }"
          @click="$emit('treat-delete', treat.id)"
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
import type { Treat } from "@/models/treat"

export default defineComponent({
  name: "TreatsItem",
  props: {
    treat: {
      type: Object as PropType<Treat>,
      required: true,
    },
    isDeleting: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["treat-delete"],
  computed: {
    discounted(): boolean {
      return this.treat.oldPrice !== null && this.treat.price < this.treat.oldPrice
    },
  },
})
</script>

<style scoped>
.is-disabled {
  opacity: 0.5;
}
</style>
