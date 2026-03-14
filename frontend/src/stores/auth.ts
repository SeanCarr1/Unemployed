import { defineStore } from 'pinia'
import api from '@/api/api'
import axios from 'axios'

type UserRole = 'seeker' | 'employer'

interface User {
  id: number
  email: string
  username: string
  role: UserRole
}

interface LoginCredentials {
  email: string
  password: string
}

interface RegisterPayload {
  username: string
  email: string
  password: string
  re_password: string
  role: UserRole
}

interface TokenPairResponse {
  access: string
  refresh: string
}

interface RefreshResponse {
  access: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
}

function parseStoredUser(): User | null {
  const rawUser = localStorage.getItem('user')
  if (!rawUser) {
    return null
  }

  try {
    const parsed = JSON.parse(rawUser) as Partial<User>
    if (
      typeof parsed.id === 'number' &&
      typeof parsed.email === 'string' &&
      typeof parsed.username === 'string' &&
      (parsed.role === 'seeker' || parsed.role === 'employer')
    ) {
      return parsed as User
    }
  } catch {
    // Ignore malformed localStorage payloads and re-authenticate.
  }

  return null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: parseStoredUser(),
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isEmployer: (state) => state.user?.role === 'employer',
    isSeeker: (state) => state.user?.role === 'seeker',
  },
  actions: {
    async login(credentials: LoginCredentials): Promise<void> {
      const response = await axios.post<TokenPairResponse>('http://localhost:8000/auth/jwt/create/', credentials)
      this.accessToken = response.data.access
      this.refreshToken = response.data.refresh
      localStorage.setItem('accessToken', this.accessToken)
      localStorage.setItem('refreshToken', this.refreshToken)
      
      // Fetch user profile after login
      await this.fetchUser()
    },
    async register(payload: RegisterPayload): Promise<void> {
      await axios.post<void>('http://localhost:8000/auth/users/', payload)
    },
    async fetchUser(): Promise<void> {
      const response = await api.get<User>('/auth/users/me/')
      this.user = response.data
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    async refreshTokens(): Promise<void> {
      if (!this.refreshToken) throw new Error('No refresh token')
      const response = await axios.post<RefreshResponse>('http://localhost:8000/auth/jwt/refresh/', {
        refresh: this.refreshToken,
      })
      this.accessToken = response.data.access
      localStorage.setItem('accessToken', this.accessToken)
    },
    logout(): void {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('user')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
  },
})
