<template>
  <div class="panel">
    <TreatsSearch v-model:search="search" />
    <TreatsTabs :active-tab="activeTab" @switch="activeTab = $event" />
    <template v-if="filteredTreats.length">
      <TreatsItem
        v-for="treat in filteredTreats"
        :key="treat.id"
        :treat="treat"
        :is-deleting="isDeleting(treat.id)"
        @treat-delete="deleteTreat"
      />
    </template>
    <template v-else>
      <div class="panel-block">
        {{ emptyText }}
      </div>
    </template>
    <NewTreat v-model:url="newTreatURL" :is-loading="isCreating" @submit="createTreat" />
  </div>
</template>

<script lang="ts">
import TreatsItem from "./TreatsItem.vue"
import TreatsTabs from "./TreatsTabs.vue"
import TreatsSearch from "./TreatsSearch.vue"
import NewTreat from "./NewTreat.vue"
import { useTreatsStore } from "@/stores/treats"
import { defineComponent } from "vue"
import type { Treat } from "@/models/treat"

const notFound = "Ни одной вкусняшки не найдено"
const empty = "Пока не добавлено ни одной вкусняшки"

export default defineComponent({
  name: "TreatsPanel",
  components: {
    NewTreat,
    TreatsItem,
    TreatsTabs,
    TreatsSearch,
  },
  setup() {
    const treatsStore = useTreatsStore()
    return { treatsStore }
  },
  data: () => {
    return {
      isCreating: false,
      deleting: [] as number[],
      search: "",
      activeTab: "ALL",
      newTreatURL: "",
    }
  },
  computed: {
    filteredTreats(): Array<Treat> {
      return this.treatsStore.treats.filter(this.filterBySearch).filter(this.filterByTab)
    },
    emptyText(): string {
      return this.treatsStore.treats.length ? notFound : empty
    },
  },
  methods: {
    isDeleting(treatId: number) {
      return this.deleting.includes(treatId)
    },
    filterBySearch(treat: Treat) {
      if (!this.search) return true
      return treat.title.toLowerCase().includes(this.search.toLowerCase())
    },
    filterByTab(treat: Treat) {
      const discounted = (treat: Treat) => treat.oldPrice !== null && treat.price < treat.oldPrice

      switch (this.activeTab) {
        case "DISCOUNTED":
          return discounted(treat)
        default:
          return true
      }
    },
    async createTreat() {
      this.isCreating = true
      let error = false

      try {
        await this.treatsStore.createTreat(this.newTreatURL)
      } catch (e) {
        error = true
        throw e
      } finally {
        this.isCreating = false

        if (!error) this.newTreatURL = ""
      }
    },
    async deleteTreat(id: number) {
      this.deleting.push(id)

      try {
        await this.treatsStore.deleteTreat(id)
      } finally {
        this.deleting = this.deleting.filter((id_) => id_ !== id)
      }
    },
  },
})
</script>
