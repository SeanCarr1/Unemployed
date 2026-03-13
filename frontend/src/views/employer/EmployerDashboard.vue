<template>
  <div class="space-y-8 py-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-4xl font-bold tracking-tight">Employer Dashboard</h1>
        <p class="text-neutral-500">Manage your job listings and applications.</p>
      </div>
      <button @click="showCreateModal = true" class="rounded-full bg-neutral-900 px-6 py-3 font-medium text-white hover:bg-neutral-800 transition-all">
        Post New Job
      </button>
    </div>

    <div class="grid gap-8 lg:grid-cols-3">
      <!-- Jobs List -->
      <div class="lg:col-span-2 space-y-4">
        <h2 class="text-xl font-bold">Your Listings</h2>
        <div v-if="jobsLoading" class="rounded-2xl border border-dashed border-neutral-200 p-12 text-center">
          <p class="text-neutral-500">Loading your listings...</p>
        </div>
        <div v-else-if="jobsError" class="rounded-2xl border border-dashed border-red-200 bg-red-50 p-12 text-center">
          <p class="text-red-700">{{ jobsError }}</p>
        </div>
        <div v-else-if="jobs.length === 0" class="rounded-2xl border border-dashed border-neutral-200 p-12 text-center">
          <p class="text-neutral-500">You haven't posted any jobs yet.</p>
        </div>
        <div v-for="job in jobs" :key="job.id" class="flex items-center justify-between rounded-2xl border border-neutral-200 bg-white p-6">
          <div>
            <h3 class="font-bold">{{ job.title }}</h3>
            <p class="text-sm text-neutral-500">{{ formatType(job.job_type) }} • {{ job.location }}</p>
          </div>
          <div class="flex gap-2">
            <button class="rounded-lg border border-neutral-200 px-4 py-2 text-sm font-medium hover:bg-neutral-50">Edit</button>
            <button @click="deleteJob(job.id)" class="rounded-lg border border-red-100 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50">Delete</button>
          </div>
        </div>
      </div>

      <!-- Recent Applications -->
      <div class="space-y-4">
        <h2 class="text-xl font-bold">Recent Applications</h2>
        <div v-if="applicationsLoading" class="rounded-2xl border border-neutral-200 bg-white p-8 text-center">
          <p class="text-sm text-neutral-500">Loading applications...</p>
        </div>
        <div v-else-if="applicationsError" class="rounded-2xl border border-red-200 bg-red-50 p-8 text-center">
          <p class="text-sm text-red-700">{{ applicationsError }}</p>
        </div>
        <div v-else-if="applications.length === 0" class="rounded-2xl border border-neutral-200 bg-white p-8 text-center">
          <p class="text-sm text-neutral-500">No applications yet.</p>
        </div>
        <div v-for="app in applications" :key="app.id" class="rounded-2xl border border-neutral-200 bg-white p-4 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">{{ app.seeker_email }}</span>
            <span :class="['rounded-full px-2 py-1 text-[10px] font-bold uppercase tracking-wider', statusColor(app.status)]">
              {{ app.status }}
            </span>
          </div>
          <p class="text-xs text-neutral-500">Applied for: {{ app.job_title }}</p>
          <div class="flex gap-2">
            <button @click="updateStatus(app.id, 'accepted')" class="flex-1 rounded-lg bg-emerald-50 py-2 text-xs font-bold text-emerald-700 hover:bg-emerald-100">Accept</button>
            <button @click="updateStatus(app.id, 'pending')" class="flex-1 rounded-lg bg-blue-50 py-2 text-xs font-bold text-blue-700 hover:bg-blue-100">Mark Pending</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Job Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/50 backdrop-blur-sm p-4">
      <div class="w-full max-w-2xl rounded-3xl bg-white p-8 shadow-2xl">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-bold">Post a New Job</h2>
          <button @click="showCreateModal = false" class="text-2xl">×</button>
        </div>

        <form @submit.prevent="handleCreateJob" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-sm font-medium">Job Title</label>
              <input v-model="jobForm.title" type="text" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
            </div>
            <div class="space-y-1">
              <label class="text-sm font-medium">Location</label>
              <input v-model="jobForm.location" type="text" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-sm font-medium">Type</label>
              <select v-model="jobForm.job_type" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none">
                <option value="full-time">Full-time</option>
                <option value="part-time">Part-time</option>
                <option value="contractual">Contractual</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-1">
                <label class="text-sm font-medium">Salary Min</label>
                <input v-model.number="jobForm.salary_min" type="number" min="0" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
              </div>
              <div class="space-y-1">
                <label class="text-sm font-medium">Salary Max</label>
                <input v-model.number="jobForm.salary_max" type="number" min="0" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
              </div>
            </div>
          </div>
          <div class="space-y-1">
            <label class="text-sm font-medium">Description</label>
            <textarea v-model="jobForm.description" rows="4" required class="w-full rounded-xl border border-neutral-200 p-4 focus:border-emerald-500 focus:outline-none"></textarea>
          </div>

          <button :disabled="creating" type="submit" class="w-full rounded-xl bg-neutral-900 py-4 font-bold text-white hover:bg-neutral-800 disabled:opacity-50">
            {{ creating ? 'Posting...' : 'Post Job' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, onMounted } from 'vue'
import type { JobPayload } from '@/api/jobsApi'
import { useAuthStore } from '@/stores/auth'
import { useJobsStore } from '@/stores/jobs'
import { useApplicationsStore } from '@/stores/applications'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const jobsStore = useJobsStore()
const applicationsStore = useApplicationsStore()
const toastStore = useToastStore()

const jobsLoading = computed(() => jobsStore.loading)
const jobsError = computed(() => jobsStore.error)
const applicationsLoading = computed(() => applicationsStore.loading)
const applicationsError = computed(() => applicationsStore.error)

const jobs = computed(() => {
  const email = authStore.user?.email
  if (!email) {
    return []
  }
  return jobsStore.items.filter((job) => job.employer_email === email)
})

const applications = computed(() => applicationsStore.items)

const showCreateModal = ref(false)
const creating = ref(false)

const jobForm = reactive<JobPayload>({
  title: '',
  location: '',
  job_type: 'full-time',
  salary_min: 0,
  salary_max: 0,
  description: '',
})

const fetchData = async () => {
  try {
    await Promise.all([
      jobsStore.fetchAll(),
      applicationsStore.fetchAll(),
    ])
  } catch (error) {
    toastStore.error('Failed to load dashboard data')
  }
}

const handleCreateJob = async () => {
  if (jobForm.salary_min > jobForm.salary_max) {
    return toastStore.error('Salary min cannot be greater than salary max')
  }

  creating.value = true
  try {
    await jobsStore.create({ ...jobForm })
    toastStore.success('Job posted successfully!')
    showCreateModal.value = false
    jobForm.title = ''
    jobForm.location = ''
    jobForm.job_type = 'full-time'
    jobForm.salary_min = 0
    jobForm.salary_max = 0
    jobForm.description = ''
    await fetchData()
  } catch (error) {
    toastStore.error('Failed to post job')
  } finally {
    creating.value = false
  }
}

const deleteJob = async (id: number) => {
  if (!confirm('Are you sure?')) return
  try {
    await jobsStore.remove(id)
    toastStore.success('Job deleted')
    await fetchData()
  } catch (error) {
    toastStore.error('Failed to delete job')
  }
}

const updateStatus = async (id: number, status: 'pending' | 'accepted') => {
  try {
    await applicationsStore.update(id, { status })
    toastStore.success(`Application ${status}`)
    await fetchData()
  } catch (error) {
    toastStore.error('Failed to update status')
  }
}

const statusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'bg-blue-50 text-blue-700'
    case 'accepted': return 'bg-emerald-50 text-emerald-700'
    default: return 'bg-neutral-50 text-neutral-700'
  }
}

const formatType = (value: string) => {
  return value.replace('-', ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

onMounted(fetchData)
</script>
