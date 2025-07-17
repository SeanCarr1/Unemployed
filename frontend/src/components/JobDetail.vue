<script setup lang="ts">
// JobList.vue: Fetches and displays all jobs, with actions for view, edit, and delete.
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useJobsStore } from '../stores/jobs'

const route = useRoute
const jobId = Number(route.params.id)
const jobsStore = useJobsStore()

onMounted(() => {
  jobsStore.fetchJob(jobId)
})


</script>

<template>
  <div>
    <h2>Job Details</h2>
    <div v-if="jobsStore.loading">Loading...</div>
    <div v-else-if="jobsStore.error" style="color: red">{{ jobsStore.error }}</div>
    <div v-else-if="jobsStore.selectedJob">
      <h3>{{ jobsStore.selectedJob.title }}</h3>
      <p>{{ jobsStore.selectedJob.description }}</p>
      <p>{{ jobsStore.selectedJob.location }}</p>
      <p>{{ jobsStore.selectedJob.salary_min }}</p>
      <p>{{ jobsStore.selectedJob.salary_max }}</p>
      <p>{{ jobsStore.selectedJob.job_type }}</p>
      <p>{{ jobsStore.selectedJob.employer_email }}</p>
      <p>{{ jobsStore.selectedJob.posted_at }}</p>
    </div>
  </div>
</template>