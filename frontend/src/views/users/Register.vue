<template>
  <div class="mx-auto max-w-md py-12">
    <div class="rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm">
      <h1 class="mb-2 text-3xl font-bold tracking-tight">Create account</h1>
      <p class="mb-8 text-neutral-500">Join the community and find your next role.</p>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-neutral-700">Username</label>
          <input v-model="form.username" type="text" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none transition-all" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-neutral-700">Email address</label>
          <input v-model="form.email" type="email" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none transition-all" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1">
            <label class="text-sm font-medium text-neutral-700">Password</label>
            <input v-model="form.password" type="password" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none transition-all" />
          </div>
          <div class="space-y-1">
            <label class="text-sm font-medium text-neutral-700">Confirm</label>
            <input v-model="form.re_password" type="password" required class="w-full rounded-xl border border-neutral-200 px-4 py-3 focus:border-emerald-500 focus:outline-none transition-all" />
          </div>
        </div>
        
        <div class="space-y-1">
          <label class="text-sm font-medium text-neutral-700">I am a...</label>
          <div class="grid grid-cols-2 gap-2">
            <button type="button" @click="form.role = 'seeker'" :class="['rounded-xl border py-3 text-sm font-medium transition-all', form.role === 'seeker' ? 'border-emerald-600 bg-emerald-50 text-emerald-700' : 'border-neutral-200 hover:bg-neutral-50']">
              Job Seeker
            </button>
            <button type="button" @click="form.role = 'employer'" :class="['rounded-xl border py-3 text-sm font-medium transition-all', form.role === 'employer' ? 'border-emerald-600 bg-emerald-50 text-emerald-700' : 'border-neutral-200 hover:bg-neutral-50']">
              Employer
            </button>
          </div>
        </div>

        <button :disabled="loading" type="submit" class="w-full rounded-xl bg-neutral-900 py-3 font-medium text-white hover:bg-neutral-800 disabled:opacity-50 transition-all">
          {{ loading ? 'Creating account...' : 'Create account' }}
        </button>
      </form>

      <p class="mt-8 text-center text-sm text-neutral-500">
        Already have an account? 
        <router-link to="/login" class="font-medium text-emerald-600 hover:underline">Sign in</router-link>
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
  username: '',
  email: '',
  password: '',
  re_password: '',
  role: 'seeker' as 'seeker' | 'employer'
})

const handleRegister = async () => {
  if (form.password !== form.re_password) {
    return toastStore.error('Passwords do not match')
  }

  loading.value = true
  try {
    await authStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
      re_password: form.re_password,
      role: form.role,
    })
    toastStore.success('Account created! Please login.')
    router.push('/login')
  } catch (error: any) {
    const errors = error.response?.data
    const firstError = errors ? Object.values(errors)[0] : 'Registration failed'
    toastStore.error(Array.isArray(firstError) ? firstError[0] : firstError)
  } finally {
    loading.value = false
  }
}
</script>
