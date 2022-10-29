<template>
  <div class="tabs" :class="tabsClasses">
    <ul>
      <li
        v-for="tab in tabs"
        :key="tab.id"
        :class="[tab.id === activeTab ? 'is-active' : '']"
        @click.prevent="emitUpdate(tab)"
      >
        <a href="">{{ tab.title }}</a>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import type { TabRecord } from "@/consts"

export default defineComponent({
  name: "AppTabs",
  props: {
    toggle: {
      type: Boolean,
      default: false,
    },
    centered: {
      type: Boolean,
      default: true,
    },
    boxed: {
      type: Boolean,
      default: false,
    },
    fullwidth: {
      type: Boolean,
      default: false,
    },
    activeTab: {
      type: String,
      default(rawProps: any) {
        return rawProps.tabs[0].id
      },
    },
    tabs: {
      type: Array as PropType<Array<TabRecord>>,
      required: true,
      validator(value: Array<TabRecord>) {
        return value.length >= 1
      },
    },
  },
  emits: ["update:tab"],
  computed: {
    tabsClasses() {
      const classes = []

      if (this.centered) classes.push("is-centered")
      if (this.boxed) classes.push("is-boxed")
      if (this.fullwidth) classes.push("is-fullwidth")
      if (this.toggle) classes.push("is-toggle")

      return classes
    },
  },
  methods: {
    emitUpdate(tab: TabRecord) {
      this.$emit("update:tab", tab.id)
    },
  },
})
</script>

<style scoped></style>
