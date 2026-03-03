// src/api/jobsCrudAdapter.ts
import { listJobs, getJob, createJob, updateJob, deleteJob } from '@/api/jobsApi'

export const jobsCrudApi = {
  list: listJobs,
  get: getJob,
  create: createJob,
  update: updateJob,
  remove: deleteJob
}