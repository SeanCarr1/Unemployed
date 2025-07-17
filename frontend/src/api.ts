import axios from 'axios'
import { useAuthStore } from './stores/auth'
import router from './router'

const api = axios.create({
    baseURL: 'http://localhost:8000/',
    headers: {
        'Content-Type': 'application/json'
    }
})


// Auto-add Authorization header
api.interceptors.request.use((config) => {
    const auth = useAuthStore()
    if (auth.token) {
        config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
})

// Intercept 401 errors and try refresh
api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config
    const auth = useAuthStore()

    if (err.response?.status === 401 && auth.refreshToken) {
      try {
        await auth.refreshAccessToken()
        originalRequest.headers.Authorization = `Bearer ${auth.token}`
        return api(originalRequest)  // retry request
        
      } catch (refreshErr) {
        auth.logout()
        router.push('/login')
        return Promise.reject(refreshErr)
      }
    }

    return Promise.reject(err)
  }
)
export default api