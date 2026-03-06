
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const re_password = ref('');
const username = ref('');
const role = ref('seeker'); // Default to job seeker
const loading = ref(false);
const errorMsg = ref('');
const auth = useAuthStore();
const router = useRouter();

const validate = () => {
    if (!email.value || !username.value || !password.value || !re_password.value) {
        errorMsg.value = 'All fields are required.';
        return false;
    }
    if (!email.value.includes('@')) {
        errorMsg.value = 'Enter a valid email.';
        return false;
    }
    if (password.value !== re_password.value) {
        errorMsg.value = 'Passwords do not match.';
        return false;
    }
    errorMsg.value = '';
    return true;
};

const register = async () => {
    if (!validate()) return;
    loading.value = true;
    errorMsg.value = '';
    try {
        await auth.register(email.value, username.value, password.value, re_password.value, role.value);
        if (auth.error) {
            errorMsg.value = auth.error;
        } else {
            router.push('/login');
        }
    } catch (err: any) {
        errorMsg.value = 'Registration failed.';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; border: 1px solid #eee; border-radius: 8px;">
        <h1 style="text-align: center;">Register</h1>
        <form v-if="!auth.user" @submit.prevent="register">
            <label>Email</label>
            <input type="email" v-model="email" required autocomplete="email" />
            <br />

            <label>Username</label>
            <input type="text" v-model="username" required autocomplete="username" />
            <br />

            <label>Password</label>
            <input type="password" v-model="password" required autocomplete="new-password" />
            <br />

            <label>Confirm Password</label>
            <input type="password" v-model="re_password" required autocomplete="new-password" />
            <br />

            <label>Role</label>
            <select v-model="role" required>
                <option value="seeker">Job Seeker</option>
                <option value="employer">Employer</option>
            </select>
            <br />

            <button type="submit" :disabled="loading" style="margin-top: 1rem;">{{ loading ? 'Registering...' : 'Register' }}</button>
        </form>
        <div v-if="errorMsg" style="color: #b91c1c; margin-top: 1rem;">{{ errorMsg }}</div>
        <div v-if="auth.user">
            <h2>Welcome {{ auth.user.username }}</h2>
            <p>Email: {{ auth.user.email }}</p>
        </div>
    </div>
</template>