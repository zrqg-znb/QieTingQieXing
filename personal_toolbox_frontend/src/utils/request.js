import axios from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    const userStore = useUserStore()

    if (error.response) {
      switch (error.response.status) {
        case 401:
          userStore.clearAuthData()
          router.push({
            name: 'login',
            query: { redirect: router.currentRoute.value.fullPath }
          })
          break
        case 403:
          router.push({ name: 'home' })
          break
        case 404:
          router.push({ name: 'not-found' })
          break
        default:
          console.error('API Error:', error.response)
      }
    } else if (error.request) {
      console.error('Network Error:', error.request)
    } else {
      console.error('Error:', error.message)
    }

    return Promise.reject(error)
  }
)

export default request