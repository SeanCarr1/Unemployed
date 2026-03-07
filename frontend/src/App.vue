<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import NavBar from '@/components/NavBar.vue';

const auth = useAuthStore()
auth.fetchUser()
</script>

<template>
  <NavBar />
  <router-view />
</template>

<style scoped>

</style>
