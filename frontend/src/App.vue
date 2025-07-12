<template>
  <div class="app-container">
    <!-- 登录和注册页面不使用主布局 -->
    <template v-if="isAuthRoute">
      <router-view />
    </template>
    
    <!-- 其他页面使用主布局 -->
    <template v-else>
      <MainLayout>
        <router-view />
      </MainLayout>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import MainLayout from '@/components/layout/MainLayout.vue';

const route = useRoute();

// 判断当前是否为认证相关路由（登录/注册）
const isAuthRoute = computed(() => {
  return [
    '/login', 
    '/register'
  ].includes(route.path);
});
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100%;
}
</style>