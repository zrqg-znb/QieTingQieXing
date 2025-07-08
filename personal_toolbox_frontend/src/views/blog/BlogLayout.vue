<template>
  <div class="blog-layout">
    <el-container>
      <el-header>
        <el-menu
          mode="horizontal"
          :router="true"
          :default-active="$route.path"
          class="blog-menu"
        >
          <el-menu-item index="/blog">
            <el-icon><Document /></el-icon>
            文章列表
          </el-menu-item>
          <el-menu-item index="/blog/editor">
            <el-icon><EditPen /></el-icon>
            写文章
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
import { Document, EditPen } from '@element-plus/icons-vue'
</script>

<style scoped>
.blog-layout {
  height: 100%;
}

.el-container {
  height: 100%;
}

.el-header {
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
}

.blog-menu {
  height: 100%;
  padding-left: 20px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}
</style>