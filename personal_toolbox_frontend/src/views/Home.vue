<template>
  <div class="home">
    <el-row :gutter="20" class="welcome-section">
      <el-col :span="24">
        <el-card class="welcome-card">
          <h1>欢迎使用个人工具箱</h1>
          <p>这是一个集成了博客系统和数据可视化功能的个人工具平台</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="feature-section">
      <el-col :span="12">
        <el-card class="feature-card" @click="$router.push('/blog')">
          <template #header>
            <div class="card-header">
              <h2>
                <el-icon><Document /></el-icon>
                博客系统
              </h2>
            </div>
          </template>
          <div class="card-content">
            <p>记录和分享您的想法、经验和知识</p>
            <ul>
              <li>支持Markdown编辑</li>
              <li>分类和标签管理</li>
              <li>评论互动功能</li>
            </ul>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="feature-card" @click="$router.push('/data-viz')">
          <template #header>
            <div class="card-header">
              <h2>
                <el-icon><TrendCharts /></el-icon>
                数据可视化
              </h2>
            </div>
          </template>
          <div class="card-content">
            <p>将您的数据转化为直观的图表和仪表盘</p>
            <ul>
              <li>多种数据源支持</li>
              <li>丰富的图表类型</li>
              <li>自定义仪表盘</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="user-section" v-if="isAuthenticated">
      <el-col :span="24">
        <el-card class="user-card">
          <template #header>
            <div class="card-header">
              <h2>
                <el-icon><User /></el-icon>
                个人中心
              </h2>
            </div>
          </template>
          <div class="card-content">
            <p>欢迎回来，{{ userProfile.username }}</p>
            <el-row :gutter="20" class="stats">
              <el-col :span="8">
                <div class="stat-item">
                  <h3>博客文章</h3>
                  <p>{{ stats.articleCount || 0 }}</p>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <h3>数据图表</h3>
                  <p>{{ stats.chartCount || 0 }}</p>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <h3>仪表盘</h3>
                  <p>{{ stats.dashboardCount || 0 }}</p>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Document, TrendCharts, User } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const handleProfileClick = () => {
  if (userStore.isAuthenticated) {
    router.push('/profile')
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-title {
  font-size: 2.5em;
  color: var(--el-text-color-primary);
  margin-bottom: 10px;
}

.welcome-subtitle {
  font-size: 1.2em;
  color: var(--el-text-color-secondary);
  margin-bottom: 30px;
}

.feature-cards {
  margin-bottom: 40px;
}

.feature-card {
  height: 100%;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 1.2em;
}

.header-icon {
  margin-right: 8px;
  font-size: 1.5em;
}

.card-content {
  text-align: left;
}

.card-content p {
  margin-bottom: 15px;
  color: var(--el-text-color-regular);
}

.card-content ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 20px;
}

.card-content ul li {
  margin-bottom: 8px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
}

.card-content ul li::before {
  content: '•';
  color: var(--el-color-primary);
  margin-right: 8px;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 2em;
  }

  .welcome-subtitle {
    font-size: 1em;
  }
}
</style>