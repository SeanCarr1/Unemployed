<template>
  <div class="mx-auto max-w-4xl py-12 space-y-12">
    <div class="flex items-center justify-between">
      <h1 class="text-4xl font-bold tracking-tight">Your Profile</h1>
      <button @click="handleUpdate" :disabled="updating" class="rounded-full bg-neutral-900 px-6 py-3 font-medium text-white hover:bg-neutral-800 disabled:opacity-50">
        {{ updating ? 'Saving...' : 'Save Changes' }}
      </button>
    </div>

    <div class="grid gap-12 md:grid-cols-3">
      <aside class="space-y-4">
        <div class="h-32 w-32 rounded-full bg-neutral-100 border border-neutral-200 overflow-hidden">
          <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${authStore.user?.username}`" alt="Avatar" class="h-full w-full object-cover" />
        </div>
        <div>
          <h2 class="text-xl font-bold">{{ authStore.user?.username }}</h2>
          <p class="text-neutral-500">{{ authStore.user?.email }}</p>
          <span class="mt-2 inline-block rounded-full bg-neutral-100 px-3 py-1 text-xs font-bold uppercase tracking-wider text-neutral-600">
            {{ authStore.user?.role }}
          </span>
        </div>
      </aside>

      <div class="md:col-span-2 space-y-8">
        <section class="space-y-4">
          <h3 class="text-lg font-bold">Account Settings</h3>
          <div class="grid gap-4 sm:grid-cols-2">
            <div class="space-y-1">
              <label class="text-sm font-medium">Username</label>
              <input v-model="form.username" type="text" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
            </div>
            <div class="space-y-1">
              <label class="text-sm font-medium">Email</label>
              <input v-model="form.email" type="email" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
            </div>
          </div>
        </section>

        <section v-if="authStore.isSeeker" class="space-y-4">
          <h3 class="text-lg font-bold">Your Applications</h3>
          <div v-if="applicationsLoading" class="rounded-2xl border border-dashed border-neutral-200 p-8 text-center">
            <p class="text-neutral-500">Loading your applications...</p>
          </div>
          <div v-else-if="applicationsError" class="rounded-2xl border border-dashed border-red-200 bg-red-50 p-8 text-center">
            <p class="text-red-700">{{ applicationsError }}</p>
          </div>
          <div v-else-if="applications.length === 0" class="rounded-2xl border border-dashed border-neutral-200 p-8 text-center">
            <p class="text-neutral-500">You haven't applied to any jobs yet.</p>
          </div>
          <div v-for="app in applications" :key="app.id" class="flex items-center justify-between rounded-2xl border border-neutral-200 bg-white p-6">
            <div>
              <h4 class="font-bold">{{ app.job_title }}</h4>
              <p class="text-sm text-neutral-500">Applied on {{ formatDate(app.applied_at) }}</p>
            </div>
            <span :class="['rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider', statusColor(app.status)]">
              {{ app.status }}
            </span>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useApplicationsStore } from '@/stores/applications'
import { useToastStore } from '@/stores/toast'
import api from '@/api/api'

const authStore = useAuthStore()
const applicationsStore = useApplicationsStore()
const toastStore = useToastStore()

const updating = ref(false)

const applications = computed(() => applicationsStore.items)
const applicationsLoading = computed(() => applicationsStore.loading)
const applicationsError = computed(() => applicationsStore.error)

const form = reactive({
  username: authStore.user?.username || '',
  email: authStore.user?.email || ''
})

const fetchData = async () => {
  if (authStore.isSeeker) {
    try {
      await applicationsStore.fetchAll()
    } catch (error) {
      toastStore.error('Failed to load your applications')
    }
  }
}

const handleUpdate = async () => {
  updating.value = true
  try {
    await api.patch('/auth/users/me/', form)
    await authStore.fetchUser()
    toastStore.success('Profile updated!')
  } catch (error) {
    toastStore.error('Failed to update profile')
  } finally {
    updating.value = false
  }
}

const statusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'bg-blue-50 text-blue-700'
    case 'accepted': return 'bg-emerald-50 text-emerald-700'
    default: return 'bg-neutral-50 text-neutral-700'
  }
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleDateString()
}

watch(
  () => authStore.user,
  (user) => {
    form.username = user?.username || ''
    form.email = user?.email || ''
  },
  { immediate: true }
)

onMounted(fetchData)
</script>
