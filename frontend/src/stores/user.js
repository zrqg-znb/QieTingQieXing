import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/utils/axios'

// 用户状态管理
export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  
  // 动作
  async function login(credentials) {
    try {
      const response = await axios.post('/api/auth/users/login/', credentials)
      setTokens(response.data.access, response.data.refresh)
      setUser(response.data.user)
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }
  
  async function register(userData) {
    try {
      const response = await axios.post('/api/auth/users/', userData)
      return response
    } catch (error) {
      console.error('注册失败:', error)
      throw error
    }
  }
  
  async function logout() {
    try {
      await axios.post('/api/auth/users/logout/')
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      clearUserData()
    }
  }
  
  async function refreshAccessToken() {
    try {
      const response = await axios.post('/api/auth/token/refresh/', {
        refresh: refreshToken.value
      })
      setTokens(response.data.access, response.data.refresh)
      return response
    } catch (error) {
      console.error('刷新令牌失败:', error)
      clearUserData()
      throw error
    }
  }
  
  async function fetchUserProfile() {
    try {
      const response = await axios.get('/api/auth/users/me/')
      setUser(response.data)
      return response
    } catch (error) {
      console.error('获取用户资料失败:', error)
      throw error
    }
  }
  
  async function updateUserProfile(profileData) {
    try {
      const response = await axios.put('/api/auth/users/update_profile/', profileData)
      setUser(response.data)
      return response
    } catch (error) {
      console.error('更新用户资料失败:', error)
      throw error
    }
  }
  
  // 辅助函数
  function setTokens(accessToken, newRefreshToken) {
    token.value = accessToken
    localStorage.setItem('token', accessToken)
    
    if (newRefreshToken) {
      refreshToken.value = newRefreshToken
      localStorage.setItem('refreshToken', newRefreshToken)
    }
  }
  
  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }
  
  function clearUserData() {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }
  
  return {
    token,
    refreshToken,
    user,
    isLoggedIn,
    login,
    register,
    logout,
    refreshAccessToken,
    fetchUserProfile,
    updateUserProfile
  }
})