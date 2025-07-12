<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>关于我们</h3>
        <p>切听切行是一个集知识库与商城于一体的平台，致力于为用户提供优质的学习资源和相关产品。</p>
      </div>
      
      <div class="footer-section">
        <h3>快速链接</h3>
        <ul>
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/wiki">知识库</router-link></li>
          <li><router-link to="/shop">商城</router-link></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h3>联系我们</h3>
        <p>邮箱：contact@qietingqiexing.com</p>
        <p>电话：400-123-4567</p>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; {{ currentYear }} 切听切行. 保留所有权利。</p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.app-footer {
  background-color: #f5f7fa;
  padding: 40px 20px 20px;
  margin-top: 40px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 30px;
}

.footer-section {
  flex: 1;
  min-width: 250px;
  
  h3 {
    font-size: 18px;
    margin-bottom: 15px;
    color: var(--el-color-primary);
  }
  
  p {
    color: #606266;
    line-height: 1.6;
    margin-bottom: 10px;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    
    li {
      margin-bottom: 8px;
      
      a {
        color: #606266;
        text-decoration: none;
        transition: color 0.3s;
        
        &:hover {
          color: var(--el-color-primary);
        }
      }
    }
  }
}

.footer-bottom {
  max-width: 1200px;
  margin: 30px auto 0;
  padding-top: 20px;
  border-top: 1px solid #dcdfe6;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 20px;
  }
  
  .footer-section {
    min-width: 100%;
  }
}
</style>