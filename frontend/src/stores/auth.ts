import { defineStore } from 'pinia'
import api from '@/api/api'
import axios from 'axios'

interface User {
  id: number
  email: string
  username: string
  role: 'seeker' | 'employer' | 'admin'
}

interface LoginCredentials {
  username: string
  password: string
}

interface RegisterPayload {
  username: string
  email: string
  password: string
  re_password: string
  role: 'seeker' | 'employer' | 'admin'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null') as User | null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isEmployer: (state) => state.user?.role === 'employer',
    isSeeker: (state) => state.user?.role === 'seeker',
    isAdmin: (state) => state.user?.role === 'admin',
  },
  actions: {
    async login(credentials: LoginCredentials) {
      const response = await axios.post('http://localhost:8000/auth/jwt/create/', credentials)
      this.accessToken = response.data.access
      this.refreshToken = response.data.refresh
      localStorage.setItem('accessToken', this.accessToken!)
      localStorage.setItem('refreshToken', this.refreshToken!)
      
      // Fetch user profile after login
      await this.fetchUser()
    },
    async register(payload: RegisterPayload) {
      await axios.post('http://localhost:8000/auth/users/', payload)
    },
    async fetchUser() {
      const response = await api.get('/auth/users/me/')
      this.user = response.data
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    async refreshTokens() {
      if (!this.refreshToken) throw new Error('No refresh token')
      const response = await axios.post('http://localhost:8000/auth/jwt/refresh/', {
        refresh: this.refreshToken,
      })
      this.accessToken = response.data.access
      localStorage.setItem('accessToken', this.accessToken!)
    },
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('user')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
  },
})
