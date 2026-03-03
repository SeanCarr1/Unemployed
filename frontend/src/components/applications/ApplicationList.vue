<script setup lang="ts">
import { onMounted } from 'vue'
import { useApplicationsStore } from '@/stores/applications'

const appStore = useApplicationsStore()

onMounted(() => {
  appStore.fetchAll()
})
</script>

<template>
  <div>
    <h2>Applications</h2>
    <div v-if="appStore.loading">Loading...</div>
    <div v-else-if="appStore.error" class="text-red-500">{{ appStore.error }}</div>
    <ul v-else>
      <li v-for="app in appStore.items" :key="app.id" class="mb-4 p-2 border-b">
        <div><strong>Position:</strong> {{ app.job_title || app.job }}</div>
        <div><strong>Status:</strong> {{ app.status }}</div>
        <div><strong>Applied At:</strong> {{ app.applied_at }}</div>
        <div><strong>Seeker:</strong> {{ app.seeker_email || app.seeker }}</div>
        <!-- Add more fields as needed -->
        <!-- You can add a router-link to detail page if needed -->
      </li>
      <li v-if="!appStore.items.length">No applications found.</li>
    </ul>
  </div>
</template>
