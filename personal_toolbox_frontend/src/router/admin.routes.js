import UserManagement from '@/views/admin/UserManagement.vue'
import SystemSettings from '@/views/admin/SystemSettings.vue'

export default [
  {
    path: '',
    children: [
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: {
          title: '用户管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'settings',
        name: 'SystemSettings',
        component: SystemSettings,
        meta: {
          title: '系统设置',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  }
]