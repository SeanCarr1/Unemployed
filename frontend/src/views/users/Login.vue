<template>
  <div class="mx-auto max-w-md py-12">
    <div class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm">
      <h1 class="mb-2 text-3xl font-bold tracking-tight">Welcome back</h1>
      <p class="mb-8 text-neutral-500">Enter your credentials to access your account.</p>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-neutral-700">Email address</label>
          <input v-model="form.email" type="email" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="name@company.com" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-neutral-700">Password</label>
          <input v-model="form.password" type="password" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 transition-all" placeholder="••••••••" />
        </div>

        <button :disabled="loading" type="submit" class="w-full rounded-xl bg-neutral-900 py-3 font-medium text-white hover:bg-neutral-800 disabled:opacity-50 transition-all">
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>

      <p class="mt-8 text-center text-sm text-neutral-500">
        Don't have an account? 
        <router-link to="/register" class="font-medium text-emerald-600 hover:underline">Create one</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()

const loading = ref(false)
const form = reactive({
  email: '',
  password: '',
})

const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.login({
      email: form.email,
      password: form.password
    })
    toastStore.success('Welcome back!')
    router.push('/')
  } catch (error: any) {
    toastStore.error(error.response?.data?.detail || 'Failed to login')
  } finally {
    loading.value = false
  }
}
</script>
