<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()
const jobId = route.params.id

const title = ref('')
const description = ref('')
const error = ref('')
const loading = ref(true)

const fetchJob = async () => {
  try {
    const res = await api.get(`/jobs/${jobId}/`)
    title.value = res.data.title
    description.value = res.data.description
  } catch (err) {
    error.value = 'Failed to load job.'
  } finally {
    loading.value = false
  }
}

const update = async () => {
  try {
    await api.patch(`/jobs/${jobId}/`, {
      title: title.value,
      description: description.value
    })
    await router.push('/dashboard/jobs')
  } catch (err) {
    error.value = 'Update failed.'
  }
}

onMounted(fetchJob)
</script>

<template>
  <div>
    <h2>Edit Job</h2>
    <div v-if="loading">Loading...</div>
    <form v-else @submit.prevent="update">
      <input v-model="title" type="text" required /><br />
      <textarea v-model="description" required></textarea><br />
      <button type="submit">Update</button>
    </form>
    <p style="color: red">{{ error }}</p>
  </div>
</template>
