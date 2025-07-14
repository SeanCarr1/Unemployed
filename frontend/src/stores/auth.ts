import { defineStore } from 'pinia' //used to create global state store
import { ref, computed } from 'vue' //vue's reactivity system for state and derived values
import api from '../api.ts'

interface User {
  username: string
  email: string
}
// Define the Auth Store
//creates a pinia store named 'auth'
export const useAuthStore = defineStore('auth', () => {
    const token = ref<string>(localStorage.getItem('access_token') || '') // stores the jwt access token initialized from localStorage if present
    const user = ref<User | null>(null) // stores the current user object or null
    const error = ref<string>('') 
    const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')

    const isAuthenticated = computed(() => !!user.value)

    const fetchUser = async () => {
    if (!token.value) return
    try {
        const res = await api.get<User>('/example/', {
        headers: {
            Authorization: `Bearer ${token.value}`,
        }
        })
        user.value = res.data
    } catch (err) {
        logout()
    }
  }

    const register = async(email: string, username: string, password: string, role: string) => {
        try {
            await api.post<{ access: string, refresh: string }>('/auth/users/', { email, username, password, role })
        } catch(err: any) {
            error.value = 'Invalid registration'
        }
    }

    const login = async (email: string, password: string) => {
        try {
            const res = await api.post<{ access: string, refresh: string }>('/token/', { email, password })
            
            token.value = res.data.access
            refreshToken.value = res.data.refresh

            localStorage.setItem('access_token', token.value)
            localStorage.setItem('refresh_token', refreshToken.value)

            await fetchUser()
            error.value = ''
        } catch (err) {
            error.value = 'Invalid credentials'
            logout()
        }
    }

    const logout = () => {
        token.value = ''
        refreshToken.value = ''
        user.value = null
        error.value = ''
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    }


    const refreshAccessToken = async () => {
        if (!refreshToken.value) return
        try {
            const res = await api.post<{ access: string }>('/token/refresh/', {
            refresh: refreshToken.value
            })
            token.value = res.data.access
            localStorage.setItem('access_token', token.value)
        } catch (err) {
            logout()
        }
    }

  return {
    token,
    user,
    error,
    isAuthenticated,
    login,
    logout,
    fetchUser
  }

  
})
