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
        <div v-if="jobs.length === 0" class="rounded-2xl border border-dashed border-neutral-200 p-12 text-center">
          <p class="text-neutral-500">You haven't posted any jobs yet.</p>
        </div>
        <div v-for="job in jobs" :key="job.id" class="flex items-center justify-between rounded-2xl border border-neutral-200 bg-white p-6">
          <div>
            <h3 class="font-bold">{{ job.title }}</h3>
            <p class="text-sm text-neutral-500">{{ job.type }} • {{ job.location }}</p>
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
        <div v-if="applications.length === 0" class="rounded-2xl border border-neutral-200 bg-white p-8 text-center">
          <p class="text-sm text-neutral-500">No applications yet.</p>
        </div>
        <div v-for="app in applications" :key="app.id" class="rounded-2xl border border-neutral-200 bg-white p-4 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold">{{ app.seeker_name }}</span>
            <span :class="['rounded-full px-2 py-1 text-[10px] font-bold uppercase tracking-wider', statusColor(app.status)]">
              {{ app.status }}
            </span>
          </div>
          <p class="text-xs text-neutral-500">Applied for: {{ app.job_title }}</p>
          <div class="flex gap-2">
            <button @click="updateStatus(app.id, 'accepted')" class="flex-1 rounded-lg bg-emerald-50 py-2 text-xs font-bold text-emerald-700 hover:bg-emerald-100">Accept</button>
            <button @click="updateStatus(app.id, 'rejected')" class="flex-1 rounded-lg bg-red-50 py-2 text-xs font-bold text-red-700 hover:bg-red-100">Reject</button>
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
              <select v-model="jobForm.type" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none">
                <option value="Full-time">Full-time</option>
                <option value="Contract">Contract</option>
                <option value="Remote">Remote</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-sm font-medium">Salary Range</label>
              <input v-model="jobForm.salary_range" type="text" placeholder="e.g. $100k - $120k" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
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
import { ref, reactive, onMounted } from 'vue'
import api from '@/api/api'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
const jobs = ref<any[]>([])
const applications = ref<any[]>([])
const showCreateModal = ref(false)
const creating = ref(false)

const jobForm = reactive({
  title: '',
  location: '',
  type: 'Full-time',
  salary_range: '',
  description: ''
})

const fetchData = async () => {
  try {
    const [jobsRes, appsRes] = await Promise.all([
      api.get('/jobs/my_jobs/'),
      api.get('/applications/received/')
    ])
    jobs.value = jobsRes.data
    applications.value = appsRes.data
  } catch (error) {
    // Mock for demo
    jobs.value = [{ id: 1, title: 'Senior Product Designer', type: 'Full-time', location: 'Remote' }]
    applications.value = [
      { id: 1, seeker_name: 'John Doe', job_title: 'Senior Product Designer', status: 'submitted' },
      { id: 2, seeker_name: 'Jane Smith', job_title: 'Senior Product Designer', status: 'reviewed' }
    ]
  }
}

const handleCreateJob = async () => {
  creating.value = true
  try {
    await api.post('/jobs/', jobForm)
    toastStore.success('Job posted successfully!')
    showCreateModal.value = false
    fetchData()
  } catch (error) {
    toastStore.error('Failed to post job')
  } finally {
    creating.value = false
  }
}

const deleteJob = async (id: number) => {
  if (!confirm('Are you sure?')) return
  try {
    await api.delete(`/jobs/${id}/`)
    toastStore.success('Job deleted')
    fetchData()
  } catch (error) {
    toastStore.error('Failed to delete job')
  }
}

const updateStatus = async (id: number, status: string) => {
  try {
    await api.patch(`/applications/${id}/`, { status })
    toastStore.success(`Application ${status}`)
    fetchData()
  } catch (error) {
    toastStore.error('Failed to update status')
  }
}

const statusColor = (status: string) => {
  switch (status) {
    case 'submitted': return 'bg-blue-50 text-blue-700'
    case 'reviewed': return 'bg-yellow-50 text-yellow-700'
    case 'accepted': return 'bg-emerald-50 text-emerald-700'
    case 'rejected': return 'bg-red-50 text-red-700'
    default: return 'bg-neutral-50 text-neutral-700'
  }
}

onMounted(fetchData)
</script>
