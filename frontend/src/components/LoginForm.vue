
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMsg = ref('');
const auth = useAuthStore();
const router = useRouter();

const validate = () => {
    if (!email.value || !password.value) {
        errorMsg.value = 'Email and password are required.';
        return false;
    }
    if (!email.value.includes('@')) {
        errorMsg.value = 'Enter a valid email.';
        return false;
    }
    errorMsg.value = '';
    return true;
};

const handleLogin = async () => {
    if (!validate()) return;
    loading.value = true;
    errorMsg.value = '';
    try {
        await auth.login(email.value, password.value);
        if (auth.error) {
            errorMsg.value = auth.error;
        } else {
            router.push('/dashboard');
        }
    } catch (err: any) {
        errorMsg.value = 'Login failed.';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; border: 1px solid #eee; border-radius: 8px;">
        <h1 style="text-align: center;">Login</h1>
        <form v-if="!auth.user" @submit.prevent="handleLogin">
            <label>Email</label>
            <input type="email" v-model="email" required autocomplete="email" />
            <br />

            <label>Password</label>
            <input type="password" v-model="password" required autocomplete="current-password" />
            <br />

            <button type="submit" :disabled="loading" style="margin-top: 1rem;">{{ loading ? 'Logging in...' : 'Login' }}</button>
        </form>
        <div v-if="errorMsg" style="color: #b91c1c; margin-top: 1rem;">{{ errorMsg }}</div>
        <div v-if="auth.user">
            <h2>Welcome {{ auth.user.email }}</h2>
            <p>Email: {{ auth.user.email }}</p>
        </div>
    </div>
</template>