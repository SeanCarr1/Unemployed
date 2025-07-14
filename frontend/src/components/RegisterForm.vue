<script setup lang=ts>

import { ref } from 'vue';

import { useAuthStore } from '@/stores/auth';

const email = ref<string>('')    
const password = ref<string>('')
const username = ref<string>('')
const auth = useAuthStore()
const role = ref<string>('seeker') // Default to job seeker

const register = async () => {
    await auth.register(email.value, username.value, password.value, role.value)
}
</script>

<template>

    <div>
        <h1>Register</h1>
        <form v-if="!auth.user" @submit.prevent="register">
            <label>Email</label>
            <input type="email" v-model="email" required>
            <br>

            <label>username</label>
            <input type="text" v-model="username" required>
            <br>

            <label>Password</label>
            <input type="password" v-model="password" required>
            <br>

            <label>Role</label>
            <select v-model="role" required>
                <option value="seeker">Job Seeker</option>
                <option value="employer">Employer</option>
            </select>
            <br />
            <button type="submit">submit</button>
        </form>
        <div v-if="auth.error" style="color: rebeccapurple;">{{ auth.error }}</div>
        <div v-if="auth.user">
            <h2>Welcome {{ auth.user.username }}</h2>
            <p>Email: {{ auth.user.email }}</p>
        </div>
    </div>
</template>