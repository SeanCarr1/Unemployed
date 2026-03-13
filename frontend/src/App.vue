<template>
  <div class="min-h-screen bg-neutral-50 font-sans text-neutral-900">
    <nav class="sticky top-0 z-50 border-b border-neutral-200 bg-white/80 backdrop-blur-md">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <router-link to="/" class="text-2xl font-bold tracking-tighter text-neutral-900">
          UNEMPLOYED<span class="text-emerald-600">.</span>
        </router-link>
        
        <div class="flex items-center gap-6">
          <router-link to="/jobs" class="text-sm font-medium hover:text-emerald-600 transition-colors">Jobs</router-link>
          
          <template v-if="authStore.isAuthenticated">
            <router-link v-if="authStore.isEmployer" to="/employer/dashboard" class="text-sm font-medium hover:text-emerald-600 transition-colors">Dashboard</router-link>
            <router-link to="/profile" class="text-sm font-medium hover:text-emerald-600 transition-colors">Profile</router-link>
            <button @click="handleLogout" class="text-sm font-medium text-red-600 hover:text-red-700 transition-colors">Logout</button>
          </template>
          
          <template v-else>
            <router-link to="/login" class="text-sm font-medium hover:text-emerald-600 transition-colors">Login</router-link>
            <router-link to="/register" class="rounded-full bg-neutral-900 px-5 py-2 text-sm font-medium text-white hover:bg-neutral-800 transition-all">Join Now</router-link>
          </template>
        </div>
      </div>
    </nav>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Toast Notifications -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
      <div v-for="toast in toastStore.toasts" :key="toast.id" 
           :class="[
             'flex items-center gap-3 rounded-xl border px-6 py-4 shadow-lg transition-all duration-300',
             toast.type === 'success' ? 'border-emerald-100 bg-emerald-50 text-emerald-900' : 'border-red-100 bg-red-50 text-red-900'
           ]">
        <span class="text-sm font-medium">{{ toast.message }}</span>
        <button @click="toastStore.remove(toast.id)" class="opacity-50 hover:opacity-100">×</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const toastStore = useToastStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  toastStore.success('Logged out successfully')
  router.push('/login')
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --font-sans: 'Inter', sans-serif;
}
</style>
