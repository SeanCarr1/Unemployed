// application.ts
// Service for applications CRUD operations using axios and Pinia auth store

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


export interface Application {
    id: number;
    job: number; // job id
    job_title?: string;
    seeker: number; // seeker id
    seeker_email?: string;
    resume: string; // URL or filename
    cover_letter: string; // URL or filename
    status: 'pending' | 'accepted';
    applied_at: string; // ISO date string
}


export interface ApplicationPayload {
    job: number;
    resume: File;
    cover_letter: File;
}

export interface ApplicationUpdatePayload {
  status: 'pending' | 'accepted';
}

export async function listApplications(): Promise<Application[]> {
  try {
    const res = await api.get<Application[] | PaginatedResponse<Application>>('/applications/')
    return Array.isArray(res.data) ? res.data : res.data.results

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function getApplication(id: number): Promise<Application> {
  try {
    const res = await api.get<Application>(`/applications/${id}/`)
    return res.data

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}


export async function createApplication(payload: ApplicationPayload): Promise<Application> {
  try {
    const formData = new FormData();
    formData.append('job', String(payload.job));
    formData.append('resume', payload.resume);
    formData.append('cover_letter', payload.cover_letter);
    const res = await api.post<Application>('/applications/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function updateApplication(id: number, payload: ApplicationUpdatePayload): Promise<Application> {
  try {
    const res = await api.patch<Application>(`/applications/${id}/`, payload)
    return res.data

  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

export async function deleteApplication(id: number): Promise<void> {
  try {
    await api.delete(`/applications/${id}/`)
    
  } catch (err: unknown) {
    rethrowApiError(err)
  }
}

function buildQuery(params: Record<string, unknown>) {
  const searchParams = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value != null) searchParams.append(key, String(value))
  })
  return `?${searchParams.toString()}`
}

export async function listApplicationsPaginated(page = 1, pageSize = 10) {
  const res = await api.get<Application[] | PaginatedResponse<Application>>(
    `/applications/${buildQuery({ page, page_size: pageSize })}`
  )
  return Array.isArray(res.data) ? res.data : res.data.results
}

export async function listApplicationsWithQuery(params: Record<string, unknown>) {
  const res = await api.get<Application[] | PaginatedResponse<Application>>(
    `/applications/${buildQuery(params)}`
  )
  return Array.isArray(res.data) ? res.data : res.data.results
}

export async function searchApplications(term: string) {
  return listApplicationsWithQuery({ search: term })
}

export async function listApplicationsByJob(jobId: number) {
  return listApplicationsWithQuery({ job: jobId })
}

export async function listMyApplications() {
  return listApplicationsWithQuery({ mine: true })
}