<script setup lang="ts">
import { ref } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const title = ref('')
const description = ref('')
const error = ref('')
const router = useRouter()

const submit = async () => {
  try {
    await api.post('/jobs/', { title: title.value, description: description.value })
    await router.push('/dashboard/jobs')
  } catch (err) {
    error.value = 'Could not create job'
  }
}
</script>

<template>
  <div>
    <h2>New Job</h2>
    <form @submit.prevent="submit">
      <input v-model="title" type="text" placeholder="Title" required /><br />
      <textarea v-model="description" placeholder="Description" required></textarea><br />
      <button type="submit">Create</button>
    </form>
    <p style="color: red">{{ error }}</p>
  </div>
</template>
