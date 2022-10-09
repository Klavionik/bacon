<template>
  <NavBar />
  <UserProfile />
</template>

<script lang="ts">
import { defineComponent } from "vue"

import UserProfile from "@/components/UserProfile.vue"
import NavBar from "@/components/NavBar.vue"
export default defineComponent({
  name: "ProfileView",
  components: { NavBar, UserProfile },
})
</script>

<style scoped></style>
