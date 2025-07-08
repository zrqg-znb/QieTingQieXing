import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    roles: JSON.parse(localStorage.getItem('roles') || '[]')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.roles.includes('admin'),
    userProfile: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        const response = await request.post('/api/auth/login/', credentials)
        this.setAuthData(response.data)
        return response
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async register(userData) {
      try {
        const response = await request.post('/api/auth/register/', userData)
        this.setAuthData(response.data)
        return response
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },

    async logout() {
      try {
        await request.post('/api/auth/logout/')
      } catch (error) {
        console.error('Logout failed:', error)
      } finally {
        this.clearAuthData()
      }
    },

    async fetchUserProfile() {
      try {
        const response = await request.get('/api/auth/profile/')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return response
      } catch (error) {
        console.error('Fetch profile failed:', error)
        throw error
      }
    },

    async updateProfile(profileData) {
      try {
        const response = await request.patch('/api/auth/profile/', profileData)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return response
      } catch (error) {
        console.error('Update profile failed:', error)
        throw error
      }
    },

    setAuthData(data) {
      this.token = data.token
      this.user = data.user
      this.roles = data.roles || []
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      localStorage.setItem('roles', JSON.stringify(data.roles || []))
      request.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
    },

    clearAuthData() {
      this.token = ''
      this.user = null
      this.roles = []
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('roles')
      delete request.defaults.headers.common['Authorization']
    }
  }
})