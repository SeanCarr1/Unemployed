// src/stores/applications.ts
import { defineStore } from 'pinia'
import { useCrudStore } from './crudFactory'
import { applicationsCrudApi } from '@/api/adapter/applications_crud'
import type { Application, ApplicationPayload } from '@/api/applications'

export const useApplicationsStore = defineStore('applications', () => {
  return useCrudStore<Application, ApplicationPayload, Partial<ApplicationPayload>>(applicationsCrudApi)
})