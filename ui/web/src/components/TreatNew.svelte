<div class="panel-block">
  <div class="is-flex width-100">
    <p class="control is-flex-grow-1">
      <input class="input" type="text" placeholder="Ссылка" bind:value={link}>
    </p>
    <p class="control ml-1">
      <button disabled={!validLink} class="button" class:is-loading={isLoading} type="submit" on:click={addTreat}>
        <span class="icon is-left" class:is-invisible={isLoading}><i class="fas fa-circle-plus has-text-primary"></i></span>
      </button>
    </p>
  </div>
</div>

<script>
  import {createEventDispatcher} from "svelte"

  const dispatch = createEventDispatcher()

  export let isLoading = false
  export let shops = []
  let link = ''

  const addTreat = () => {
    dispatch('add', link)
  }

  $: validPatterns = shops.map((shop) => new RegExp(shop["link_pattern"]))
  $: validLink = validPatterns.every((pattern) => pattern.test(link))
</script>

<style>
  .width-100 {
    width: 100%;
  }
</style>