import axios from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// 创建axios实例
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    
    // 如果有token，则添加到请求头
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const userStore = useUserStore()
    
    // 如果是401错误（未授权），可能是token过期
    if (error.response && error.response.status === 401) {
      const originalRequest = error.config
      
      // 防止无限循环：如果已经尝试过刷新token，则直接登出
      if (originalRequest._retry) {
        userStore.logout()
        router.push('/login')
        return Promise.reject(error)
      }
      
      // 尝试刷新token
      if (userStore.refreshToken) {
        originalRequest._retry = true
        
        try {
          await userStore.refreshAccessToken()
          
          // 更新原始请求的token
          originalRequest.headers.Authorization = `Bearer ${userStore.token}`
          
          // 重试原始请求
          return instance(originalRequest)
        } catch (refreshError) {
          // 如果刷新token失败，则登出并跳转到登录页
          userStore.logout()
          router.push('/login')
          return Promise.reject(refreshError)
        }
      } else {
        // 如果没有刷新token，则直接登出
        userStore.logout()
        router.push('/login')
      }
    }
    
    return Promise.reject(error)
  }
)

export default instance