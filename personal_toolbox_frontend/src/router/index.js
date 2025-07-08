import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/index.vue'
import blogRoutes from './blog.routes'
import dataVizRoutes from './data-viz.routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue'),
      meta: {
        title: '首页'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/Register.vue')
    },
    {
      path: '/blog',
      name: 'blog',
      component: () => import('../views/blog/BlogLayout.vue'),
      children: [
        {
          path: '',
          name: 'blog-list',
          component: () => import('../views/blog/ArticleList.vue')
        },
        {
          path: 'article/:slug',
          name: 'article-detail',
          component: () => import('../views/blog/ArticleDetail.vue')
        },
        {
          path: 'new',
          name: 'article-new',
          component: () => import('../views/blog/ArticleEditor.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'edit/:slug',
          name: 'article-edit',
          component: () => import('../views/blog/ArticleEditor.vue'),
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/data-viz',
      name: 'data-viz',
      component: () => import('../views/data-viz/DataVizLayout.vue'),
      children: [
        {
          path: '',
          redirect: '/data-viz/dashboards'
        },
        {
          path: 'dashboard/:id',
          name: 'dashboard-detail',
          component: () => import('../views/data-viz/DashboardDetail.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'charts',
          name: 'chart-list',
          component: () => import('../views/data-viz/ChartList.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'data-sources',
          name: 'data-source-list',
          component: () => import('../views/data-viz/DataSourceList.vue'),
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: 'users',
          name: 'user-management',
          component: () => import('../views/admin/UserManagement.vue')
        },
        {
          path: 'settings',
          name: 'system-settings',
          component: () => import('../views/admin/SystemSettings.vue')
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router