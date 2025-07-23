// src/stores/jobs.ts
import { defineStore } from 'pinia'
import { useCrudStore } from './crudFactory'
import { jobsCrudApi } from '@/api/adapter/jobs_crud'
import type { Job, JobPayload } from '@/api/jobsApi'

export const useJobsStore = defineStore('jobs', () => {
  return useCrudStore<Job, JobPayload, Partial<JobPayload>>(jobsCrudApi)
})