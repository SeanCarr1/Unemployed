<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useJobsStore } from '../stores/jobs'


const jobsStore = useJobsStore()
const router = useRouter()

const title = ref<string>('')
const description = ref<string>('') 
const location = ref<string>('') 
const salary_min = ref<number | null>(null)
const salary_max = ref<number | null>(null)
const job_type = ref<string>('') 

async function createJob() {
  try {
    await jobsStore.createJob({
      title: title.value,
      description: description.value,
      location: location.value,
      salary_min: salary_min.value ?? 0,
      salary_max: salary_max.value ?? 0,
      job_type: job_type.value
    })
    router.push('/jobs')
  } catch (err) {
    // error is set in store
  }
}
</script>

<template>
  <div>
    <h2>Create Job</h2>
    <div v-if="jobsStore.error" class="text-red-500">{{ jobsStore.error }}</div>
    <div v-if="jobsStore.loading">Loading job...</div>
    <form v-else @submit.prevent="createJob">
      <label>Title:</label>
      <input v-model="title" type="text" required /><br />

      <label>Description:</label>
      <textarea v-model="description" required></textarea><br />

      <label>Location:</label>
      <input v-model="location" type="text" required /><br />

      <label>Salary Min:</label>
      <input v-model.number="salary_min" type="number" required /><br />

      <label>Salary Max:</label>
      <input v-model.number="salary_max" type="number" required /><br />

      <label>Job Type:</label>
      <select v-model="job_type" required>
        <option value="full-time">Full-time</option>
        <option value="part-time">Part-time</option>
        <option value="contractual">Contractual</option>
      </select><br />
      
      <button type="submit">Create Job</button>
    </form>
  </div>
</template>

