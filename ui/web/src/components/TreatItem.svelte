<article class="panel-block" class:is-disabled={isLoading}>
  <div class="media is-flex-grow-1">
    <div class="media-content pl-3">
      <div class="content">
        <p>
          <strong>{title}</strong> <a class="tag is-light is-info" href="{url}">{shopName}</a>
          <br>
          <span>Цена:
            {#if discount}<del>{lastPrice} &#8381;</del> {/if}{price} &#8381;</span>
        </p>
      </div>
    </div>
    <div class="my-auto">
      <button class="button is-inverted is-outlined is-danger" class:is-loading={isLoading} on:click={() => deleteTreat(id)}>
        <span class="icon" class:is-invisible={isLoading}><i class="delete has-background-danger"></i></span>
      </button>
    </div>
  </div>
</article>

<script>
  import {createEventDispatcher} from "svelte"

  const dispatch = createEventDispatcher()

  export let id
  export let title
  export let price
  export let lastPrice
  export let shopName
  export let url
  export let isLoading = false

  $: discount = (lastPrice !== null) && (price < lastPrice)

  const deleteTreat = (id) => {
    dispatch('delete', id)
  }
</script>

<style>
  .is-disabled {
    opacity: 0.5;
  }
</style>