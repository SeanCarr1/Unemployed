<script setup lang="ts">
// JobList.vue: Fetches and displays all jobs, with actions for view, edit, and delete.
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useJobsStore } from '@/stores/jobs'

const route = useRoute()
const jobId = Number(route.params.id)
const jobsStore = useJobsStore()

onMounted(() => {
  jobsStore.fetchOne(jobId)
})


</script>

<template>
  <div>
    <h2>Job Details</h2>
    <div v-if="jobsStore.loading">Loading...</div>
    <div v-else-if="jobsStore.error" style="color: red">{{ jobsStore.error }}</div>
    <div v-else-if="jobsStore.selected">
      <h3>{{ jobsStore.selected.title }}</h3>
      <p>{{ jobsStore.selected.description }}</p>
      <p>{{ jobsStore.selected.location }}</p>
      <p>{{ jobsStore.selected.salary_min }}</p>
      <p>{{ jobsStore.selected.salary_max }}</p>
      <p>{{ jobsStore.selected.job_type }}</p>
      <p>{{ jobsStore.selected.employer_email }}</p>
      <p>{{ jobsStore.selected.posted_at }}</p>
    </div>
  </div>
</template>