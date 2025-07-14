
<script setup lang="ts">
// JobList.vue: Fetches and displays all jobs, with actions for view, edit, and delete.
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

// Define the Job type based on your backend model fields
interface Job {
  id: number
  title: string
  description: string
  location: string
  salary_min: number
  salary_max: number
  job_type: string
  posted_at: string
  // employer: number | string // Uncomment if you want to display employer info
}

const jobs = ref<Job[]>([])
const error = ref<string>('')
const loading = ref<boolean>(true)
const router = useRouter()

// Fetch all jobs from the API on component mount
onMounted(async () => {
  try {
    const response = await api.get<Job[]>('/jobs/')
    jobs.value = response.data
    error.value = ''
  } catch (err: any) {
    error.value = 'Failed to load jobs.'
  } finally {
    loading.value = false
  }
})

// Navigate to the job detail page
function viewJob(id: number) {
  router.push(`/jobs/${id}`)
}

// Navigate to the job edit page
function editJob(id: number) {
  router.push(`/jobs/${id}/edit`)
}

// Delete a job with confirmation
async function deleteJob(id: number) {
  if (!window.confirm('Are you sure you want to delete this job?')) return
  try {
    await api.delete(`/jobs/${id}/`)
    jobs.value = jobs.value.filter(job => job.id !== id)
    error.value = ''
  } catch (err: any) {
    error.value = 'Failed to delete job.'
  }
}
</script>

<template>
  <div>
    <h2>Job List</h2>
    <div v-if="error" style="color: red;">{{ error }}</div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="jobs.length === 0">No jobs found.</div>
      <div v-for="job in jobs" :key="job.id" style="border: 1px solid #ccc; margin-bottom: 1rem; padding: 1rem;">
        <h3>{{ job.title }}</h3>
        <ul>
          <li><strong>Description:</strong> {{ job.description }}</li>
          <li><strong>Location:</strong> {{ job.location }}</li>
          <li><strong>Salary:</strong> {{ job.salary_min }} - {{ job.salary_max }}</li>
          <li><strong>Type:</strong> {{ job.job_type }}</li>
          <li><strong>Posted At:</strong> {{ job.posted_at }}</li>
        </ul>
        <button @click="viewJob(job.id)">View</button>
        <button @click="editJob(job.id)">Edit</button>
        <button @click="deleteJob(job.id)">Delete</button>
      </div>
    </div>
  </div>
</template>
