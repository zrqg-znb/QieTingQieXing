<template>
  <el-container class="app-container">
    <el-header height="60px">
      <nav class="nav-header">
        <div class="logo-container">
          <router-link to="/" class="logo">
            <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
            <span class="logo-text">个人知识与工具库</span>
          </router-link>
        </div>
        
        <el-menu
          mode="horizontal"
          :router="true"
          class="nav-menu"
          :ellipsis="false"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>首页
          </el-menu-item>
          <el-menu-item index="/blog">
            <el-icon><Document /></el-icon>博客
          </el-menu-item>
          <el-menu-item index="/data-viz">
            <el-icon><TrendCharts /></el-icon>数据可视化
          </el-menu-item>
          
          <!-- 管理员菜单 -->
          <el-menu-item 
            v-if="userStore.isAdmin" 
            index="/admin"
          >
            <el-icon><Setting /></el-icon>系统管理
          </el-menu-item>
        </el-menu>

        <div class="user-menu">
          <template v-if="userStore.isAuthenticated">
            <el-dropdown>
              <span class="user-profile">
                <el-avatar 
                  :size="32" 
                  :src="userStore.userProfile?.avatar || ''"
                />
                <span class="username">{{ userStore.userProfile?.username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="router.push('/profile')">
                    <el-icon><User /></el-icon>个人信息
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="text" @click="router.push('/login')">
              登录
            </el-button>
            <el-button type="primary" @click="router.push('/register')">
              注册
            </el-button>
          </template>
        </div>
      </nav>
    </el-header>

    <el-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer height="60px">
      <div class="footer-content">
        <p>&copy; {{ new Date().getFullYear() }} 个人知识与工具库. All rights reserved.</p>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { House, Document, TrendCharts, Setting, User, SwitchButton } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = async () => {
  try {
    await userStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/login')
  } catch (error) {
    ElMessage.error('退出登录失败')
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.nav-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--el-text-color-primary);
}

.logo-image {
  height: 32px;
  margin-right: 10px;
}

.logo-text {
  font-size: 1.2em;
  font-weight: bold;
}

.nav-menu {
  flex: 1;
  justify-content: center;
  border-bottom: none;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
}

.footer-content {
  text-align: center;
  color: var(--el-text-color-secondary);
  padding: 20px 0;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
