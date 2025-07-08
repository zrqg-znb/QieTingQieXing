<template>
  <div class="app-layout">
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <div class="left">
            <router-link to="/" class="logo">
              <img src="@/assets/logo.svg" alt="Logo" />
              <span>个人工具箱</span>
            </router-link>

            <el-menu
              mode="horizontal"
              :router="true"
              :default-active="$route.path"
              class="main-nav"
            >
              <el-menu-item index="/">
                <el-icon><House /></el-icon>首页
              </el-menu-item>
              <el-menu-item index="/blog">
                <el-icon><Document /></el-icon>博客
              </el-menu-item>
              <el-menu-item index="/data-viz">
                <el-icon><DataLine /></el-icon>数据可视化
              </el-menu-item>
              <el-menu-item index="/admin" v-if="isAdmin">
                <el-icon><Setting /></el-icon>系统管理
              </el-menu-item>
            </el-menu>
          </div>

          <div class="right">
            <template v-if="isAuthenticated">
              <el-dropdown trigger="click" @command="handleCommand">
                <div class="user-info">
                  <el-avatar :size="32" :src="userAvatar" />
                  <span class="username">{{ username }}</span>
                  <el-icon><CaretBottom /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon>个人信息
                    </el-dropdown-item>
                    <el-dropdown-item command="settings">
                      <el-icon><Setting /></el-icon>账号设置
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <el-button type="primary" @click="handleLogin">登录</el-button>
              <el-button @click="handleRegister">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>

      <el-main>
        <router-view></router-view>
      </el-main>

      <el-footer height="60px">
        <div class="footer-content">
          <p>&copy; {{ currentYear }} 个人工具箱. All rights reserved.</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  House,
  Document,
  DataLine,
  Setting,
  CaretBottom,
  User,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)
const isAdmin = computed(() => userStore.isAdmin)
const username = computed(() => userStore.userProfile?.username)
const userAvatar = computed(() => userStore.userProfile?.avatar)
const currentYear = computed(() => new Date().getFullYear())

const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      await userStore.logout()
      router.push('/login')
      break
  }
}

const handleLogin = () => {
  router.push('/login')
}

const handleRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--el-text-color-primary);
  margin-right: 40px;
}

.logo img {
  height: 32px;
  margin-right: 10px;
}

.logo span {
  font-size: 20px;
  font-weight: bold;
}

.main-nav {
  border-bottom: none;
}

.right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: var(--el-fill-color-light);
}

.username {
  margin: 0 8px;
  color: var(--el-text-color-primary);
}

.el-main {
  padding: 0;
  background-color: var(--el-fill-color-light);
}

.el-footer {
  background-color: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-light);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--el-text-color-secondary);
}
</style>