import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import { API_BASE_URL } from '@/api/config'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore()
    const originalRequest = error.config

    if (
      error.response?.status === 401 &&
      authStore.refreshToken &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true
      try {
        await authStore.refreshTokens()
        originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
        return api(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export default api
