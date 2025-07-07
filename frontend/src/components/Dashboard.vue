<script setup lang="ts">

import { useAuthStore } from '@/stores/auth';
const auth = useAuthStore()
</script>

<template>
    <div>
        <h1>Dashboard</h1>
        <p>Welcome, {{ auth.user?.username }}</p>
        <button @click="auth.logout">Logout</button>
    </div>
</template>