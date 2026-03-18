<!-- JobDetail.vue - Job details -->
<template>
  <div v-if="job" class="mx-auto max-w-4xl py-12">
    <div class="mb-12 flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
      <div class="flex gap-6">
        <div class="h-20 w-20 shrink-0 rounded-3xl bg-white border border-neutral-200 p-4 shadow-sm">
          <img :src="`https://picsum.photos/seed/job${job.id}/200/200`" alt="Logo" class="h-full w-full object-contain" />
        </div>
        <div>
          <h1 class="text-4xl font-bold tracking-tight">{{ job.title }}</h1>
          <p class="text-lg text-neutral-500">{{ job.company_name }} • {{ job.location }}</p>
          <div class="mt-4 flex flex-wrap gap-2">
            <span class="rounded-full bg-emerald-50 px-4 py-1 text-sm font-medium text-emerald-700">{{ job.type }}</span>
            <span class="rounded-full bg-neutral-100 px-4 py-1 text-sm font-medium text-neutral-700">{{ job.salary_range }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="authStore.isSeeker">
        <button @click="showApplyModal = true" class="rounded-full bg-emerald-600 px-8 py-4 text-lg font-bold text-white hover:bg-emerald-700 transition-all shadow-lg shadow-emerald-500/20">
          Apply for this role
        </button>
      </div>
    </div>

    <div class="grid gap-12 lg:grid-cols-3">
      <div class="lg:col-span-2 space-y-8">
        <section>
          <h2 class="mb-4 text-xl font-bold">About the role</h2>
          <div class="prose prose-neutral max-w-none text-neutral-600">
            {{ job.description }}
          </div>
        </section>
        
        <section>
          <h2 class="mb-4 text-xl font-bold">Requirements</h2>
          <ul class="list-inside list-disc space-y-2 text-neutral-600">
            <li v-for="req in job.requirements" :key="req">{{ req }}</li>
          </ul>
        </section>
      </div>

      <aside class="space-y-6">
        <div class="rounded-3xl border border-neutral-200 bg-white p-6">
          <h3 class="mb-4 font-bold">Job Overview</h3>
          <div class="space-y-4 text-sm">
            <div class="flex justify-between">
              <span class="text-neutral-500">Posted on</span>
              <span class="font-medium">March 1, 2024</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-500">Location</span>
              <span class="font-medium">{{ job.location }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-500">Experience</span>
              <span class="font-medium">Mid-Senior</span>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Apply Modal -->
    <div v-if="showApplyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/50 backdrop-blur-sm p-4">
      <div class="w-full max-w-lg rounded-3xl bg-white p-8 shadow-2xl">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-bold">Apply to {{ job.company_name }}</h2>
          <button @click="showApplyModal = false" class="text-2xl">×</button>
        </div>

        <form @submit.prevent="handleApply" class="space-y-6">
          <div class="space-y-1">
            <label class="text-sm font-medium">Cover Letter (PDF)</label>
            <div class="relative flex items-center justify-center rounded-xl border-2 border-dashed border-neutral-200 p-8 hover:border-emerald-500 transition-all cursor-pointer">
              <input type="file" @change="handleCoverLetterUpload" class="absolute inset-0 opacity-0 cursor-pointer" accept=".pdf" />
              <div class="text-center">
                <p class="text-sm font-medium text-neutral-600">{{ applyForm.cover_letter ? applyForm.cover_letter.name : 'Click or drag to upload' }}</p>
                <p class="text-xs text-neutral-400">PDF up to 5MB</p>
              </div>
            </div>
          </div>
          
          <div class="space-y-1">
            <label class="text-sm font-medium">Resume (PDF)</label>
            <div class="relative flex items-center justify-center rounded-xl border-2 border-dashed border-neutral-200 p-8 hover:border-emerald-500 transition-all cursor-pointer">
              <input type="file" @change="handleFileUpload" class="absolute inset-0 opacity-0 cursor-pointer" accept=".pdf" />
              <div class="text-center">
                <p class="text-sm font-medium text-neutral-600">{{ applyForm.resume ? applyForm.resume.name : 'Click or drag to upload' }}</p>
                <p class="text-xs text-neutral-400">PDF up to 5MB</p>
              </div>
            </div>
          </div>

          <button :disabled="applying" type="submit" class="w-full rounded-xl bg-neutral-900 py-4 font-bold text-white hover:bg-neutral-800 disabled:opacity-50">
            {{ applying ? 'Submitting...' : 'Submit Application' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useApplicationsStore } from '@/stores/applications'
import { useToastStore } from '@/stores/toast'
import api from '@/api/api'

const route = useRoute()
const authStore = useAuthStore()
const applicationsStore = useApplicationsStore()
const toastStore = useToastStore()

const job = ref<any>(null)
const showApplyModal = ref(false)
const applying = ref(false)
const applyForm = reactive({
  cover_letter: null as File | null,
  resume: null as File | null
})

const fetchJob = async () => {
  try {
    const response = await api.get(`/jobs/${route.params.id}/`)
    job.value = response.data
  } catch (error) {
    toastStore.error('Failed to load job details.')
  }
}

onMounted(fetchJob)

const handleFileUpload = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files && files.length > 0) {
    applyForm.resume = files[0]
  }
}

const handleCoverLetterUpload = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files && files.length > 0) {
    applyForm.cover_letter = files[0]
  }
}

const handleApply = async () => {
  if (!job.value?.id) {
    return toastStore.error('Job reference is missing.')
  }

  if (!applyForm.resume) {
    return toastStore.error('Please upload your resume.')
  }

  if (!applyForm.cover_letter) {
    return toastStore.error('Please upload your cover letter file.')
  }

  applying.value = true
  try {
    await applicationsStore.create({
      job: Number(job.value.id),
      resume: applyForm.resume,
      cover_letter: applyForm.cover_letter,
    })

    toastStore.success('Application submitted!')
    showApplyModal.value = false
    applyForm.resume = null
    applyForm.cover_letter = null
  } catch (error) {
    const err = error as { detail?: string; message?: string }
    toastStore.error(err.detail || err.message || 'Failed to submit application.')
  } finally {
    applying.value = false
  }
}
</script>
