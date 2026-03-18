<!-- JobList.vue - List jobs -->
<template>
  <div class="space-y-8 py-8">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-4xl font-bold tracking-tight">Browse Jobs</h1>
        <p class="text-muted-foreground">Showing {{ paginatedJobs.length }} of {{ filteredJobs.length }} open positions.</p>
      </div>

      <div class="grid w-full max-w-xl gap-2 sm:grid-cols-[1fr_180px]">
        <Input
          v-model="filters.search"
          type="text"
          placeholder="Search roles, location, or keywords"
        />

        <Select v-model="filters.type">
          <SelectTrigger>
            <SelectValue placeholder="All Types" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="full-time">Full-time</SelectItem>
            <SelectItem value="contract">Contract</SelectItem>
            <SelectItem value="remote">Remote</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <Separator />

    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card v-for="i in 6" :key="i">
        <CardHeader class="space-y-3">
          <Skeleton class="h-5 w-3/4" />
          <Skeleton class="h-4 w-1/2" />
        </CardHeader>
        <CardContent class="space-y-3">
          <Skeleton class="h-4 w-full" />
          <Skeleton class="h-4 w-11/12" />
          <Skeleton class="h-4 w-3/4" />
        </CardContent>
        <CardFooter class="flex items-center justify-between">
          <Skeleton class="h-4 w-24" />
          <Skeleton class="h-8 w-20" />
        </CardFooter>
      </Card>
    </div>

    <div v-else-if="error" class="py-10">
      <Alert variant="destructive">
        <AlertTitle>Could not load jobs</AlertTitle>
        <AlertDescription>{{ error }}</AlertDescription>
      </Alert>
      <Button class="mt-4" variant="outline" @click="fetchJobs">
        Retry
      </Button>
    </div>

    <div v-else-if="filteredJobs.length === 0" class="py-10">
      <Alert>
        <AlertTitle>No jobs found</AlertTitle>
        <AlertDescription>
          Try a broader keyword or switch the job type filter.
        </AlertDescription>
      </Alert>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card
        v-for="job in paginatedJobs"
        :key="job.id"
        class="transition-shadow duration-200 hover:shadow-md"
      >
        <CardHeader class="gap-2">
          <div class="flex items-center justify-between gap-3">
            <CardTitle class="line-clamp-1 text-lg">{{ job.title }}</CardTitle>
            <Badge variant="outline">{{ formatType(job.job_type) }}</Badge>
          </div>
          <CardDescription>
            {{ companyLabel(job.employer_email) }} • {{ job.location }}
          </CardDescription>
        </CardHeader>

        <CardContent>
          <p class="line-clamp-3 text-sm text-muted-foreground">
            {{ job.description }}
          </p>
        </CardContent>

        <CardFooter class="items-center justify-between gap-2">
          <span class="text-sm font-medium">{{ salaryLabel(job.salary_min, job.salary_max) }}</span>
          <Button as-child variant="link" class="px-0">
            <RouterLink :to="`/jobs/${job.id}`">View details</RouterLink>
          </Button>
        </CardFooter>
      </Card>
    </div>

    <div v-if="totalPages > 1" class="pt-2">
      <Pagination
        v-model:page="page"
        :items-per-page="pageSize"
        :total="filteredJobs.length"
        :sibling-count="1"
        show-edges
      >
        <PaginationContent v-slot="{ items }">
          <PaginationPrevious />

          <template v-for="(item, index) in items" :key="`page-item-${index}`">
            <PaginationItem
              v-if="item.type === 'page'"
              :value="item.value"
              :is-active="item.value === page"
            >
              {{ item.value }}
            </PaginationItem>
            <PaginationEllipsis v-else :index="index" />
          </template>

          <PaginationNext />
        </PaginationContent>
      </Pagination>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious
} from '@/components/ui/pagination'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'

import { useJobsStore } from '@/stores/jobs'
import type { Job } from '@/api/jobsApi'

const jobsStore = useJobsStore()

const page = ref(1)
const pageSize = 9
const filters = reactive({
  search: '',
  type: 'all'
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
  const matchesType = type === 'all' || normalizedType.includes(type)

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
