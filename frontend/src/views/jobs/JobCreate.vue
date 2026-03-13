<template>
  <div class="mx-auto max-w-3xl space-y-6 py-10">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Create Job</h1>
        <p class="text-neutral-500">Publish a new listing for candidates.</p>
      </div>
      <router-link to="/employer/dashboard" class="rounded-full border border-neutral-200 px-4 py-2 text-sm font-medium hover:bg-neutral-50">
        Back
      </router-link>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-5 rounded-2xl border border-neutral-200 bg-white p-6">
      <div class="grid gap-4 sm:grid-cols-2">
        <div class="space-y-1">
          <label class="text-sm font-medium">Title</label>
          <input v-model="form.title" type="text" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium">Location</label>
          <input v-model="form.location" type="text" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
        </div>
      </div>

      <div class="grid gap-4 sm:grid-cols-3">
        <div class="space-y-1">
          <label class="text-sm font-medium">Job Type</label>
          <select v-model="form.job_type" class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none">
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contractual">Contractual</option>
          </select>
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium">Salary Min</label>
          <input v-model.number="form.salary_min" type="number" min="0" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium">Salary Max</label>
          <input v-model.number="form.salary_max" type="number" min="0" required class="w-full rounded-xl border border-neutral-200 px-4 py-2 focus:border-emerald-500 focus:outline-none" />
        </div>
      </div>

      <div class="space-y-1">
        <label class="text-sm font-medium">Description</label>
        <textarea v-model="form.description" rows="6" required class="w-full rounded-xl border border-neutral-200 p-4 focus:border-emerald-500 focus:outline-none"></textarea>
      </div>

      <button :disabled="submitting" type="submit" class="w-full rounded-xl bg-neutral-900 py-3 font-medium text-white hover:bg-neutral-800 disabled:opacity-50">
        {{ submitting ? 'Publishing...' : 'Publish Job' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { JobPayload } from '@/api/jobsApi'
import { useJobsStore } from '@/stores/jobs'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const jobsStore = useJobsStore()
const toastStore = useToastStore()
const submitting = ref(false)

const form = reactive<JobPayload>({
  title: '',
  description: '',
  location: '',
  salary_min: 0,
  salary_max: 0,
  job_type: 'full-time',
})

// Validates and submits the create job form.
const handleSubmit = async () => {
  if (form.salary_min > form.salary_max) {
    return toastStore.error('Salary min cannot be greater than salary max')
  }

  submitting.value = true
  try {
    await jobsStore.create({ ...form })
    toastStore.success('Job created successfully')
    router.push('/employer/dashboard')
  } catch (error: any) {
    toastStore.error(error?.detail || error?.message || 'Failed to create job')
  } finally {
    submitting.value = false
  }
}
</script>
