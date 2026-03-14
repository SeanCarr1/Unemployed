// jobsApi.ts
// Service for job CRUD operations using axios and Pinia auth store
// All errors are thrown for toast notifications

import api from '@/api/api'

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

function rethrowApiError(err: unknown): never {
  if (typeof err === 'object' && err !== null) {
    const maybeErr = err as { response?: { data?: unknown } }
    if (typeof maybeErr.response?.data !== 'undefined') {
      throw maybeErr.response.data
    }
  }
  throw err
}

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
    const res = await api.get<Job[] | PaginatedResponse<Job>>('/jobs/')
    return Array.isArray(res.data) ? res.data : res.data.results

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function getJob(id: number): Promise<Job> {
  try {
    const res = await api.get<Job>(`/jobs/${id}/`)
    return res.data

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function createJob(payload: JobPayload): Promise<Job> {
  try {
    const res = await api.post<Job>('/jobs/', payload)
    return res.data
  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function updateJob(id: number, payload: Partial<JobPayload>): Promise<Job> {
  try {
    const res = await api.patch<Job>(`/jobs/${id}/`, payload)
    return res.data

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function deleteJob(id: number): Promise<void> {
  try {
    await api.delete(`/jobs/${id}/`)
    
  } catch (err: unknown) {
    rethrowApiError(err)
  }
}
