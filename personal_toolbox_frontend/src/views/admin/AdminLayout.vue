<template>
  <div class="admin-layout">
    <el-container>
      <el-header>
        <el-menu
          mode="horizontal"
          :router="true"
          :default-active="$route.path"
          class="admin-menu"
        >
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            用户管理
          </el-menu-item>
          <el-menu-item index="/admin/settings">
            <el-icon><Setting /></el-icon>
            系统设置
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { User, Setting } from '@element-plus/icons-vue'
</script>

<style scoped>
.admin-layout {
  height: 100%;
}

.el-container {
  height: 100%;
}

.el-header {
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
}

.admin-menu {
  height: 100%;
  padding-left: 20px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}
</style>