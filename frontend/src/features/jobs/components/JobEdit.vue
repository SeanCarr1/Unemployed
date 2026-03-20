<template>
  <div class="max-w-3xl mx-auto py-8">
    <JobForm v-if="selectedJob" :job="selectedJob" />
    <p v-else class="text-center text-neutral-500">Loading job...</p>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useJobsStore } from '@/stores/jobs'
import JobForm from '@/features/jobs/components/jobForm.vue'
import type { Job } from '@/api/jobsApi'


const route = useRoute()
const router = useRouter()
const jobsStore = useJobsStore()

const selectedJob = ref<Job | null>(null)
const jobId = Number(route.params.id)

onMounted(async () => {
  if (Number.isNaN(jobId)) {
    router.replace('/employer/dashboard')
    return
  }
  await jobsStore.fetchOne(jobId)
  if (!jobsStore.selected) {
    router.replace('/employer/dashboard')
    return
  }
  selectedJob.value = jobsStore.selected
})
</script>
