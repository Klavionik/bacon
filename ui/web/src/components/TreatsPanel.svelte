<div class="panel">
  <TreatsHeading/>
  <TreatsSearch on:search={setSearch}/>
  <TreatsTabs on:switch={setTab} bind:currentTab={currentTab}/>
  {#each filteredTreats as treat}
    <TreatItem {...treat} on:delete={deleteTreat} isLoading="{isDeleting(treat.id)}"/>
  {:else}
    <div class="panel-block">{emptyText}</div>
  {/each}
  <TreatNew on:add={createTreat} isLoading="{isCreating}" shops={shops}/>
</div>

<script>
  import {onMount} from "svelte"
  import TreatsHeading from "./TreatsHeading.svelte"
  import TreatsSearch from "./TreatsSearch.svelte"
  import TreatsTabs from "./TreatsTabs.svelte"
  import TreatItem from "./TreatItem.svelte"
  import TreatNew from "./TreatNew.svelte"
  import {Tab} from "../const.js"
  import treatService from "../services/api.js"

  export let apiService
  let isCreating = false
  let isDeletingList = []
  let treats = []
  let shops = []
  let search = '';
  let currentTab = Tab.ALL

  onMount(async () => {
    shops = await apiService.listShops().json()
    treats = await apiService.listUserTreats().json()
    treats.forEach(treat => {
      treat.shopName = shops.find(shop => shop.id === treat['shop_id']).name
      treat.lastPrice = treat['last_price']
      delete treat['last_price']
      delete treat['shop_id']
    })
  })

  const bySearch = (treat) => {
    if (!search) true
    return treat.title.toLowerCase().includes(search.toLowerCase())
  }

  const byTab = (treat) => {
    const discounted = (treat) => (treat.oldPrice !== null) && (treat.price < treat.oldPrice)

    switch (currentTab) {
      case Tab.DISCOUNTED:
        return discounted(treat)
      default:
        return true
    }
  }

  const setSearch = (event) => {
    search = event.detail
  }

  const setTab = (event) => {
    currentTab = event.detail
  }

  const deleteTreat = async (event) => {
    isDeletingList = [...isDeletingList, event.detail]
    await apiService.deleteTreat(event.detail)
    isDeletingList = isDeletingList.filter((id) => id !== event.detail)
    treats = treats.filter((treat) => treat.id !== event.detail)
  }

  const createTreat = async (event) => {
    isCreating = true

    try {
      const response = await apiService.createTreat(event.detail)
      treats = [...treats, await response.json()]
    } finally {
      isCreating = false
    }
  }

  const notFound = 'Ни одной вкусняшки не найдено'
  const empty = 'Пока не добавлено ни одной вкусняшки'

  $: filteredTreats = treats.filter((treat) => bySearch(treat, search)).filter((treat) => byTab(treat, currentTab))
  $: emptyText = search || currentTab !== Tab.ALL ? notFound : empty
  $: isDeleting = (id) => isDeletingList.includes(id)
</script>
