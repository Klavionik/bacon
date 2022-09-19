<p class="panel-tabs">
  <a class:is-active={all} on:click={() => switchTab(Tab.ALL)}>Все</a>
  <a class:is-active={discount} on:click={() => switchTab(Tab.DISCOUNTED)}>Со скидкой</a>
</p>

<script>
  import {createEventDispatcher} from "svelte"
  import {Tab} from "../const.js"

  const dispatch = createEventDispatcher()

  export let currentTab

  $: all = currentTab === Tab.ALL
  $: discount = currentTab === Tab.DISCOUNTED

  const switchTab = (tab) => {
    dispatch('switch', tab)
  }
</script>