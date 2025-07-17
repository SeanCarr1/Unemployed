import { defineStore } from 'pinia'

import type { Job, JobPayload } from '../jobsApi'
import { listJobs, getJob, createJob, updateJob, deleteJob } from '../jobsApi'

export const useJobsStore = defineStore('jobs', {
  state: () => ({
    jobs: [] as Job[],
    selectedJob: null as Job | null,
    loading: false,
    error: null as string | null,
  }), 
  actions: {
    async fetchJobs() {
      this.loading = true
      this.error = null
      try {
        this.jobs = await listJobs()
      } catch (err: any) {
        this.error = err.detail || err.message || 'Failed to fetch jobs'
      } finally {
        this.loading = false
      }
    },

    async fetchJob(id: number) {
      this.loading = true
      this.error = null
      try {
        this.selectedJob = await getJob(id)
      } catch (err: any) {
        this.error = err.detail || err.message || 'Failed to fetch job'
      } finally {
        this.loading = false
      }
    },

    async createJob(payload: JobPayload) {
      this.loading = true
      this.error = null
      try {
        const job = await createJob(payload)
        this.jobs.push(job)
        return job

      } catch (err: any) {
        this.error = err.detail || err.message || 'Failed to create job'
        throw err

      } finally {
        this.loading = false
      }
    },

    async updateJob(id: number, payload: Partial<JobPayload>) {
      this.loading = true
      this.error = null

      try {
        const job = await updateJob(id, payload)
        // Update job in jobs array
        const idx = this.jobs.findIndex(j => j.id === id)

        if (idx !== -1) this.jobs[idx] = job
        if (this.selectedJob?.id === id) this.selectedJob = job
        return job

      } catch (err: any) {
        this.error = err.detail || err.message || 'Failed to update job'
        throw err

      } finally {
        this.loading = false
      }
    },

    async deleteJob(id: number) {
      this.loading = true
      this.error = null
      try {
        await deleteJob(id)
        this.jobs = this.jobs.filter(j => j.id !== id)
        if (this.selectedJob?.id === id) this.selectedJob = null
        
      } catch (err: any) {
        this.error = err.detail || err.message || 'Failed to delete job'
        throw err

      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
