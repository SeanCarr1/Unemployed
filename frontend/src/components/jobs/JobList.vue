
<script setup lang="ts">
// JobList.vue: Fetches and displays all jobs, with actions for view, edit, and delete.
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useJobsStore } from '@/stores/jobs'

const jobsStore = useJobsStore()
const router = useRouter()

// Fetch all jobs from the API on component mount
onMounted(() => {
  jobsStore.fetchAll()
})
function viewJob(id: number) {
  router.push(`/jobs/${id}`)
}

function editJob(id: number) {
  router.push(`/jobs/${id}/edit`)
}

async function deleteJob(id: number) {
  if (!window.confirm('Are you sure you want to delete this job?')) return
  try {
    await jobsStore.remove(id)
    jobsStore.clearError()
  } catch (err: any) {
    // error is set in store
  }
}
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Job Listings</h1>
    <div v-if="jobsStore.error" class="text-red-500">{{ jobsStore.error }}</div>
    <div v-if="jobsStore.loading">Loading jobs...</div>
    <div v-else>
      <ul>
        <li v-for="job in jobsStore.items.filter(j => j && j.id)" :key="job.id" class="mb-4 border-b pb-2">
          <div class="font-semibold">{{ job.title }}</div>
          <div>{{ job.location }} | {{ job.job_type }}</div>
          <div>Salary: {{ job.salary_min }} - {{ job.salary_max }}</div>
          <div class="text-sm text-gray-500">Posted by: {{ job.employer_email }}</div>
          <button @click="viewJob(job.id)" class="text-blue-600 underline mr-2">View</button>
          <button @click="editJob(job.id)" class="text-green-600 underline mr-2">Edit</button>
          <button @click="deleteJob(job.id)" class="text-red-600 underline">Delete</button>
        </li>
      </ul>
      <div v-if="jobsStore.items.length === 0" class="text-gray-500">No jobs found.</div>
    </div>
  </div>
</template>
