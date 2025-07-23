// jobsApi.ts
// Service for job CRUD operations using axios and Pinia auth store
// All errors are thrown for toast notifications

import api from '@/api/api'

export interface Job {
  id: number
  title: string
  description: string
  location: string
  salary_min: number
  salary_max: number
  job_type: string
  employer_email?: string
  posted_at?: string
}

export interface JobPayload {
  title: string
  description: string
  location: string
  salary_min: number
  salary_max: number
  job_type: string
}

export async function listJobs(): Promise<Job[]> {
  try {
    const res = await api.get<Job[]>('/jobs/')
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function getJob(id: number): Promise<Job> {
  try {
    const res = await api.get<Job>(`/jobs/${id}/`)
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function createJob(payload: JobPayload): Promise<Job> {
  try {
    const res = await api.post<Job>('/jobs/', payload)
    return res.data
  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function updateJob(id: number, payload: Partial<JobPayload>): Promise<Job> {
  try {
    const res = await api.patch<Job>(`/jobs/${id}/`, payload)
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function deleteJob(id: number): Promise<void> {
  try {
    await api.delete(`/jobs/${id}/`)
    
  } catch (err: any) {
    throw err.response?.data || err
  }
}
