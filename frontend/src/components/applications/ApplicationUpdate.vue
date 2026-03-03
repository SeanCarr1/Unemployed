<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useApplicationsStore } from '@/stores/applications'
import { useRouter, useRoute } from 'vue-router'

const appStore = useApplicationsStore()
const router = useRouter()
const route = useRoute()

const id = ref<number | null>(null)
const application = ref<any>(null)

const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  id.value = Number(route.params.id)
  if (!id.value) {
    error.value = 'Invalid application ID.'
    return
  }
  loading.value = true
  try {
    application.value = await appStore.fetchOne(id.value)
  } catch (e: any) {
    error.value = e?.response?.data?.error || 'Failed to load application.'
  } finally {
    loading.value = false
  }
})

const status = ref('pending')
const cover_letter = ref('')

watch(application, (app) => {
  if (app) {
    status.value = app.status
    cover_letter.value = app.cover_letter
  }
})

async function updateApplication() {
  if (!id.value) return
  loading.value = true
  error.value = null
  try {
    await appStore.update(id.value, {
      status: status.value,
      cover_letter: cover_letter.value
    })
    router.push('/applications')
  } catch (e: any) {
    error.value = e?.response?.data?.error || 'Failed to update application.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h2>Update Application</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <form v-else-if="application" @submit.prevent="updateApplication">
      <label>Status:</label>
      <select v-model="status" required>
        <option value="pending">Pending</option>
        <option value="accepted">Accepted</option>
      </select><br />

      <label>Cover Letter:</label>
      <textarea v-model="cover_letter" required></textarea><br />

      <button type="submit">Update Application</button>
    </form>
    <div v-else>No application found.</div>
  </div>
</template>
