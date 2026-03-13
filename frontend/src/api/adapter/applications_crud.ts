// src/api/applicationsCrudAdapter.ts
import { listApplications, getApplication, createApplication, updateApplication, deleteApplication } from '@/api/applications'

export const applicationsCrudApi = {
  list: listApplications,
  get: getApplication,
  create: createApplication,
  update: updateApplication,
  remove: deleteApplication
}