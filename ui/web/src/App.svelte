<script>
  import {onMount} from "svelte"
  import botService from "./services/bot.js"
  import APIService from "./services/api.js";
  import TreatsPanel from "./components/TreatsPanel.svelte"
  import Forbidden from "./components/Forbidden.svelte"

  export let initData = null
  let loggedIn = false
  let forbidden = false
  let apiService = null

  onMount(start)

  async function start() {
    try {
      const { token } = await botService.start(initData).json()
      apiService = new APIService(import.meta.env.TREATS_SERVER_URL, '/api', token)
      loggedIn = true
    } catch (e) {
      if (e?.response?.status === 403) {
        forbidden = true
      }
      throw e
    }
  }

</script>

<main>
  <div class="columns is-gapless">
    <div class="column">
      {#if loggedIn}
        <TreatsPanel apiService={apiService}/>
      {/if}

      {#if forbidden}
        <Forbidden/>
      {/if}
    </div>
  </div>
</main>
