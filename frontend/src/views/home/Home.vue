
<template>
  <div class="space-y-24 py-12">
    <!-- Hero Section -->
    <section class="text-center space-y-8">
      <h1 class="text-6xl font-bold tracking-tighter sm:text-7xl lg:text-8xl">
        Find your next <br />
        <span class="text-emerald-600 italic serif">great adventure.</span>
      </h1>
      <p class="mx-auto max-w-2xl text-lg text-neutral-500">
        The minimal job board for the modern workforce. No fluff, just opportunities.
      </p>
      <div class="flex justify-center gap-4">
        <router-link to="/jobs" class="rounded-full bg-neutral-900 px-8 py-4 text-lg font-medium text-white hover:bg-neutral-800 transition-all">
          Browse Jobs
        </router-link>
        <router-link to="/register" class="rounded-full border border-neutral-200 bg-white px-8 py-4 text-lg font-medium hover:bg-neutral-50 transition-all">
          Post a Job
        </router-link>
      </div>
    </section>

    <!-- Featured Jobs -->
    <section class="space-y-8">
      <div class="flex items-end justify-between">
        <div>
          <h2 class="text-3xl font-bold tracking-tight">Latest Openings</h2>
          <p class="text-neutral-500">Hand-picked opportunities for you.</p>
        </div>
        <router-link to="/jobs" class="text-sm font-medium text-emerald-600 hover:underline">View all jobs →</router-link>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div v-if="loading" v-for="i in 3" :key="`skeleton-${i}`" class="h-56 animate-pulse rounded-2xl bg-neutral-100"></div>
        <div v-else-if="error" class="col-span-full rounded-2xl border border-red-200 bg-red-50 p-6 text-center">
          <p class="text-red-700">{{ error }}</p>
        </div>
        <div v-else-if="featuredJobs.length === 0" class="col-span-full rounded-2xl border border-dashed border-neutral-200 p-6 text-center">
          <p class="text-neutral-500">No openings available right now.</p>
        </div>
        <div v-else v-for="job in featuredJobs" :key="job.id" class="group relative rounded-2xl border border-neutral-200 bg-white p-6 transition-all hover:border-emerald-200 hover:shadow-xl hover:shadow-emerald-500/5">
          <div class="mb-4 flex items-center justify-between">
            <div class="h-12 w-12 rounded-xl bg-neutral-100 p-2">
              <img :src="`https://picsum.photos/seed/company${job.id}/100/100`" alt="Logo" class="h-full w-full object-contain grayscale group-hover:grayscale-0 transition-all" />
            </div>
            <span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">{{ formatType(job.job_type) }}</span>
          </div>
          <h3 class="text-xl font-bold group-hover:text-emerald-600 transition-colors">{{ job.title }}</h3>
          <p class="text-sm text-neutral-500">{{ companyLabel(job.employer_email) }} • {{ job.location }}</p>
          <div class="mt-6 flex items-center justify-between">
            <span class="text-sm font-medium">{{ salaryLabel(job.salary_min, job.salary_max) }}</span>
            <router-link :to="`/jobs/${job.id}`" class="text-sm font-bold text-neutral-900">Apply Now</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useJobsStore } from '@/stores/jobs'

const jobsStore = useJobsStore()

const loading = computed(() => jobsStore.loading)
const error = computed(() => jobsStore.error)
const featuredJobs = computed(() => jobsStore.items.slice(0, 3))

const salaryLabel = (min: number, max: number) => {
  return `$${Number(min).toLocaleString()} - $${Number(max).toLocaleString()}`
}

const companyLabel = (email?: string) => {
  return email ?? 'Company'
}

const formatType = (value: string) => {
  return value.replace('-', ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

onMounted(async () => {
  await jobsStore.fetchAll()
})
</script>
