<script setup lang="ts">

import { ref } from 'vue';

import { useAuthStore } from '@/stores/auth';

const email = ref<string>('')    
const password = ref<string>('')
const auth = useAuthStore()


const handleLogin = async () => {
    await auth.login(email.value, password.value)
}
</script>

<template>
    <div>
        <h1>Login</h1>    
        <form v-if="!auth.user" @submit.prevent="handleLogin">
            <label for="">Email</label>
            <input v-model="email" type="email" required/>
            <br/>

            <label for="">Password</label>
            <input type="password" v-model="password" required/>

            <button type="submit">Login</button>
        </form>

        <div v-if="auth.error" style="color: rebeccapurple;">{{ auth.error }}</div>
        <div v-if="auth.user">
            <h2>Welcome {{ auth.user.email }}</h2>
            <p>Email: {{ auth.user.email }}</p>
        </div>
    </div>
    
</template>