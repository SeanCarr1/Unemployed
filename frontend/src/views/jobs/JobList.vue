<!-- JobList.vue - List jobs -->
<template>
  <div class="space-y-8 py-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-4xl font-bold tracking-tight">Browse Jobs</h1>
        <p class="text-neutral-500">Showing {{ paginatedJobs.length }} of {{ filteredJobs.length }} open positions.</p>
      </div>
      
      <div class="flex gap-2">
        <input v-model="filters.search" type="text" placeholder="Search roles..." class="rounded-full border border-neutral-200 bg-white px-6 py-2 text-sm focus:border-emerald-500 focus:outline-none transition-all" />
        <select v-model="filters.type" class="rounded-full border border-neutral-200 bg-white px-6 py-2 text-sm focus:border-emerald-500 focus:outline-none transition-all">
          <option value="">All Types</option>
          <option value="full-time">Full-time</option>
          <option value="contract">Contract</option>
          <option value="remote">Remote</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 6" :key="i" class="h-64 animate-pulse rounded-2xl bg-neutral-100"></div>
    </div>

    <div v-else-if="error" class="py-24 text-center">
      <p class="text-lg text-red-600">{{ error }}</p>
      <button @click="fetchJobs" class="mt-4 rounded-full bg-neutral-900 px-6 py-2 text-sm font-medium text-white hover:bg-neutral-800 transition-all">
        Retry
      </button>
    </div>

    <div v-else-if="filteredJobs.length === 0" class="py-24 text-center">
      <p class="text-lg text-neutral-500">No jobs found matching your criteria.</p>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="job in paginatedJobs" :key="job.id" class="group relative rounded-2xl border border-neutral-200 bg-white p-6 transition-all hover:border-emerald-200 hover:shadow-xl">
        <div class="mb-4 flex items-center justify-between">
          <div class="h-12 w-12 rounded-xl bg-neutral-100 p-2">
            <img :src="`https://picsum.photos/seed/job${job.id}/100/100`" alt="Logo" class="h-full w-full object-contain grayscale group-hover:grayscale-0" />
          </div>
          <span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">{{ formatType(job.job_type) }}</span>
        </div>
        <h3 class="text-xl font-bold group-hover:text-emerald-600 transition-colors">{{ job.title }}</h3>
        <p class="text-sm text-neutral-500">{{ companyLabel(job.employer_email) }} • {{ job.location }}</p>
        <p class="mt-4 line-clamp-2 text-sm text-neutral-600">{{ job.description }}</p>
        <div class="mt-6 flex items-center justify-between">
          <span class="text-sm font-medium text-neutral-900">{{ salaryLabel(job.salary_min, job.salary_max) }}</span>
          <router-link :to="`/jobs/${job.id}`" class="text-sm font-bold text-emerald-600">Details →</router-link>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 pt-8">
      <button v-for="p in totalPages" :key="p" @click="page = p" :class="['h-10 w-10 rounded-full text-sm font-medium transition-all', page === p ? 'bg-neutral-900 text-white' : 'bg-white border border-neutral-200 hover:bg-neutral-50']">
        {{ p }}
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useJobsStore } from '@/stores/jobs'
import type { Job } from '@/api/jobsApi'

const jobsStore = useJobsStore()

const page = ref(1)
const pageSize = 9
const filters = reactive({
  search: '',
  type: ''
})

const loading = computed(() => jobsStore.loading)
const error = computed(() => jobsStore.error)

const filteredJobs = computed(() => {
  const search = filters.search.trim().toLowerCase()
  const type = filters.type.trim().toLowerCase()

  return jobsStore.items.filter((job) => {
    const matchesSearch =
      !search ||
      job.title.toLowerCase().includes(search) ||
      job.description.toLowerCase().includes(search) ||
      job.location.toLowerCase().includes(search)

    const normalizedType = job.job_type.toLowerCase()
    const matchesType = !type || normalizedType.includes(type)

    return matchesSearch && matchesType
  })
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredJobs.value.length / pageSize))
})

const paginatedJobs = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredJobs.value.slice(start, start + pageSize)
})

const fetchJobs = async () => {
  await jobsStore.fetchAll()
}

watch(
  () => [filters.search, filters.type],
  () => {
    page.value = 1
  }
)

watch(totalPages, (value) => {
  if (page.value > value) {
    page.value = value
  }
})

const salaryLabel = (min: number, max: number): string => {
  return `$${min.toLocaleString()} - $${max.toLocaleString()}`
}

const companyLabel = (email?: string): string => {
  return email ?? 'Company'
}

const formatType = (value: Job['job_type']): string => {
  return value.replace('-', ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

onMounted(fetchJobs)
</script>
