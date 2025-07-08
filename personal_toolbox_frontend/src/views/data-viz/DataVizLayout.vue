<template>
  <div class="data-viz-layout">
    <el-menu
      mode="horizontal"
      :router="true"
      class="sub-nav"
      :default-active="$route.path"
    >
      <el-menu-item index="/data-viz">
        <el-icon><DataLine /></el-icon>
        仪表盘
      </el-menu-item>
      <el-menu-item index="/data-viz/charts">
        <el-icon><PieChart /></el-icon>
        图表管理
      </el-menu-item>
      <el-menu-item index="/data-viz/sources">
        <el-icon><DataAnalysis /></el-icon>
        数据源管理
      </el-menu-item>
    </el-menu>

    <div class="content-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { DataLine, PieChart, DataAnalysis } from '@element-plus/icons-vue'
</script>

<style scoped>
.data-viz-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sub-nav {
  border-bottom: 1px solid var(--el-border-color-light);
  padding: 0 20px;
}

.content-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>