import request from '@/utils/request'
import * as blog from './blog'
import * as dataViz from './data-viz'

// 用户认证相关接口
export const auth = {
  login: (credentials) => request.post('/api/auth/login/', credentials),
  register: (userData) => request.post('/api/auth/register/', userData),
  logout: () => request.post('/api/auth/logout/'),
  getProfile: () => request.get('/api/auth/profile/'),
  updateProfile: (data) => request.patch('/api/auth/profile/', data)
}

// 管理员相关接口
export const admin = {
  getUsers: () => request.get('/api/admin/users/'),
  getUser: (id) => request.get(`/api/admin/users/${id}/`),
  createUser: (data) => request.post('/api/admin/users/', data),
  updateUser: (id, data) => request.put(`/api/admin/users/${id}/`, data),
  deleteUser: (id) => request.delete(`/api/admin/users/${id}/`),
  getSystemSettings: () => request.get('/api/admin/settings/'),
  updateSystemSettings: (data) => request.put('/api/admin/settings/', data)
}

export { blog, dataViz }

// 默认导出所有API
export default {
  auth,
  admin,
  blog,
  dataViz
}