<div class="panel-block">
  <p class="control has-icons-left">
    <input bind:value={search} class="input" type="text" placeholder="Поиск" on:input={emitSearch}>
    <span class="icon is-left"><i class="fas fa-search"></i></span>
  </p>
</div>

<script>
  import {createEventDispatcher} from 'svelte';

  const dispatch = createEventDispatcher();

  let search;

  const emitSearch = () => {
    dispatch('search', search)
  }
</script>