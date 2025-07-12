<template>
  <el-menu
    :default-active="activeIndex"
    class="navbar"
    mode="horizontal"
    router
    :ellipsis="false"
  >
    <div class="logo-container">
      <router-link to="/">
        <img src="@/assets/images/logo.svg" alt="切听切行" class="logo" />
        <span class="site-name">切听切行</span>
      </router-link>
    </div>
    
    <div class="flex-grow" />
    
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/wiki">知识库</el-menu-item>
    <el-menu-item index="/shop">商城</el-menu-item>
    
    <template v-if="userStore.isLoggedIn">
      <el-sub-menu index="user">
        <template #title>
          <el-avatar 
            :size="32" 
            :src="userStore.userInfo?.avatar || defaultAvatar"
          />
          <span class="username">{{ userStore.userInfo?.username }}</span>
        </template>
        <el-menu-item index="/profile">个人资料</el-menu-item>
        <el-menu-item @click="handleLogout">退出登录</el-menu-item>
      </el-sub-menu>
    </template>
    
    <template v-else>
      <el-menu-item index="/login">登录</el-menu-item>
      <el-menu-item index="/register">注册</el-menu-item>
    </template>
  </el-menu>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessageBox } from 'element-plus';
import { useUserStore } from '@/stores/user';
import defaultAvatarSrc from '@/assets/images/default-avatar.svg';

const defaultAvatar = defaultAvatarSrc;

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

// 计算当前激活的导航项
const activeIndex = computed(() => {
  const path = route.path;
  if (path.startsWith('/wiki')) return '/wiki';
  if (path.startsWith('/shop')) return '/shop';
  if (path === '/profile') return 'user';
  return path;
});

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    await userStore.logout();
    router.push('/login');
  } catch (e) {
    // 用户取消操作，不做任何处理
  }
};
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  
  a {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--el-color-primary);
  }
  
  .logo {
    height: 32px;
    margin-right: 10px;
  }
  
  .site-name {
    font-size: 18px;
    font-weight: bold;
  }
}

.flex-grow {
  flex-grow: 1;
}

.username {
  margin-left: 8px;
}

@media (max-width: 768px) {
  .site-name {
    display: none;
  }
  
  .username {
    display: none;
  }
}
</style>