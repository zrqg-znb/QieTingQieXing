import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/wiki',
    name: 'wiki',
    component: () => import('@/views/wiki/WikiHome.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wiki/article/:id',
    name: 'article-detail',
    component: () => import('@/views/wiki/ArticleDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shop',
    name: 'shop',
    component: () => import('@/views/shop/ShopHome.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shop/product/:id',
    name: 'product-detail',
    component: () => import('@/views/shop/ProductDetail.vue'),
    meta: { requiresAuth: true }
  },

  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/user/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue'),
    meta: { requiresAuth: false }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局前置守卫，用于处理身份验证
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查路由是否需要身份验证
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    // 如果需要身份验证但用户未登录，则重定向到登录页面
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    // 否则继续导航
    next()
  }
})

export default router