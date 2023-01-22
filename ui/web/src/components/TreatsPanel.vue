<template>
  <div class="panel">
    <TreatsSearch v-model:search="search" />
    <TreatsTabs :active-tab="activeTab" @switch="activeTab = $event" />
    <template v-if="noShopsConfigured">
      <div class="panel-block is-justify-content-center">
        <article class="message is-small is-warning mb-0">
          <div class="message-body">
            Прежде чем начать добавлять вкусняшки, нужно
            <RouterLink :to="{ name: 'shops' }">выбрать магазины</RouterLink>, в которых мы будем
            следить за ценами.
          </div>
        </article>
      </div>
    </template>
    <template v-else-if="filteredTreats.length">
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
import { useTreatsStore } from "@/stores/treat"
import { defineComponent } from "vue"
import type { Treat } from "@/models/treat"
import { useShopLocationsStore } from "@/stores/shop-location"
import { RouterLink } from "vue-router"
import { useUserStore } from "@/stores/user"
import { mapState, mapActions } from "pinia"

const notFound = "Ни одной вкусняшки не найдено"
const empty = "Пока не добавлено ни одной вкусняшки"

export default defineComponent({
  name: "TreatsPanel",
  components: {
    NewTreat,
    TreatsItem,
    TreatsTabs,
    TreatsSearch,
    RouterLink,
  },
  data() {
    return {
      isCreating: false,
      deleting: [] as number[],
      search: "",
      activeTab: "Все",
      newTreatURL: "",
    }
  },
  computed: {
    ...mapState(useUserStore, ["user"]),
    ...mapState(useTreatsStore, ["treats"]),
    ...mapState(useShopLocationsStore, ["userShopLocations"]),
    filteredTreats(): Array<Treat> {
      return this.treats.filter(this.filterBySearch).filter(this.filterByTab)
    },
    emptyText(): string {
      return this.treats.length ? notFound : empty
    },
    noShopsConfigured(): boolean {
      return !this.userShopLocations.length
    },
  },
  methods: {
    ...mapActions(useTreatsStore, ["create", "delete"]),
    isDeleting(treatId: number) {
      return this.deleting.includes(treatId)
    },
    filterBySearch(treat: Treat): boolean {
      if (!this.search) return true
      return treat.title.toLowerCase().includes(this.search.toLowerCase())
    },
    filterByTab(treat: Treat): boolean {
      const discounted = (treat: Treat) => treat.oldPrice !== null && treat.price < treat.oldPrice

      switch (this.activeTab) {
        case "Все":
          return true
        case "Со скидкой":
          return discounted(treat)
        default:
          return treat.shopTitle === this.activeTab
      }
    },
    async createTreat() {
      this.isCreating = true
      let error = false

      try {
        await this.create(this.user.id, this.newTreatURL)
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
        await this.delete(id)
      } finally {
        this.deleting = this.deleting.filter((id_) => id_ !== id)
      }
    },
  },
})
</script>

<style scoped>
.panel {
  border-radius: 0;
}
</style>
