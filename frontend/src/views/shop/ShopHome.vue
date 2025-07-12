<template>
  <div class="shop-container">
    <el-card class="empty-shop-card">
      <div class="empty-shop-content">
        <el-empty description="商城功能正在开发中" />
        <p class="coming-soon-text">敬请期待</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped lang="scss">
.shop-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.empty-shop-card {
  margin-bottom: 20px;
}

.empty-shop-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
}

.coming-soon-text {
  margin-top: 20px;
  font-size: 18px;
  color: #909399;
}
</style>