// application.ts
// Service for applications CRUD operations using axios and Pinia auth store

import api from '@/api/api'


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

export async function listApplications(): Promise<Application[]> {
  try {
    const res = await api.get<Application[]>('/applications/')
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function getApplication(id: number): Promise<Application> {
  try {
    const res = await api.get<Application>(`/applications/${id}/`)
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
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
  } catch (err: any) {
    throw err.response?.data || err;
  }
}

export async function updateApplication(id: number, payload: Partial<Application>): Promise<Application> {
  try {
    const res = await api.patch<Application>(`/applications/${id}/`, payload)
    return res.data

  } catch (err: any) {
    throw err.response?.data || err
  }
}

export async function deleteApplication(id: number): Promise<void> {
  try {
    await api.delete(`/applications/${id}/`)
    
  } catch (err: any) {
    throw err.response?.data || err
  }
}
