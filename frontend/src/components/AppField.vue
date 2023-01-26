<template>
  <div class="field">
    <div class="control">
      <input
        v-bind="$attrs"
        :value="modelValue"
        class="input"
        :class="{ 'is-danger': hasErrors }"
        @input="emitUpdate"
        @blur="touch"
      />
    </div>
    <p v-for="error of errors" :key="error.$uid" class="help" :class="{ 'is-danger': hasErrors }">
      {{ error.$message }}
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import type { Validation } from "@vuelidate/core"

export default defineComponent({
  name: "AppField",
  inheritAttrs: false,
  props: {
    name: {
      type: String,
      required: true,
    },
    modelValue: {
      type: String,
      default: "",
    },
    validator: {
      type: Object as PropType<Validation>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  computed: {
    errors() {
      return this.validator[this.name].$errors
    },
    hasErrors() {
      return this.validator[this.name].$errors.length
    },
  },
  methods: {
    emitUpdate(event: any) {
      this.$emit("update:modelValue", event.target.value)
    },
    touch() {
      this.modelValue.length && this.validator[this.name].$touch()
    },
  },
})
</script>

<style scoped></style>
