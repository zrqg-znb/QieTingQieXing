import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/utils/axios'

// 菜单状态管理
export const useMenuStore = defineStore('menu', () => {
  // 状态
  const menus = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // 计算属性
  const hasMenus = computed(() => menus.value.length > 0)
  
  // 动作
  async function fetchMenus() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/auth/menus/user_menus/')
      menus.value = response.data
      return response.data
    } catch (err) {
      console.error('获取菜单失败:', err)
      error.value = err.message || '获取菜单失败'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // 重置状态
  function resetMenus() {
    menus.value = []
    loading.value = false
    error.value = null
  }
  
  return {
    menus,
    loading,
    error,
    hasMenus,
    fetchMenus,
    resetMenus
  }
})