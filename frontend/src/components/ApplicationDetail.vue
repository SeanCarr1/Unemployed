<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="application">
      <h2>Application Details</h2>
      <p><strong>Position:</strong> {{ application.position || application.job_title }}</p>
      <p><strong>Applicant:</strong> {{ application.seeker_email || application.seeker }}</p>
      <p><strong>Status:</strong> {{ application.status }}</p>
      <p><strong>Cover Letter:</strong></p>
      <pre>{{ application.cover_letter }}</pre>
      <p v-if="application.resume"><strong>Resume:</strong> {{ application.resume }}</p>
      <p v-if="application.applied_at"><strong>Applied At:</strong> {{ application.applied_at }}</p>
    </div>
    <div v-else>
      <p>No application data.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch } from 'vue'

interface Application {
  id: number
  job?: number
  job_title?: string
  seeker?: number
  seeker_email?: string
  resume?: string
  cover_letter: string
  status: string
  applied_at?: string
}

defineProps<{
  application?: Application | null
  loading?: boolean
  error?: string | null
}>()
</script>
