<template>
  <div class="product-detail-container">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="error" class="error-container">
      <el-empty description="加载商品信息失败">
        <template #description>
          <p>{{ error }}</p>
        </template>
        <el-button type="primary" @click="fetchProduct">重试</el-button>
      </el-empty>
    </div>
    
    <div v-else-if="product" class="product-detail">
      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/shop' }">商城</el-breadcrumb-item>
        <el-breadcrumb-item>{{ product.name }}</el-breadcrumb-item>
      </el-breadcrumb>
      
      <div class="product-content">
        <div class="product-image">
          <img :src="product.image || defaultProductImage" :alt="product.name">
        </div>
        
        <div class="product-info">
          <h1 class="product-name">{{ product.name }}</h1>
          <div class="product-meta">
            <span class="product-id">商品编号: {{ product.id }}</span>
            <span class="product-time">上架时间: {{ formatDate(product.created_at) }}</span>
          </div>
          
          <div class="product-price">¥{{ product.price.toFixed(2) }}</div>
          
          <div class="product-description">
            <h3>商品描述</h3>
            <p>{{ product.description }}</p>
          </div>
          

        </div>
      </div>
    </div>
    
    <div v-else class="empty-container">
      <el-empty description="商品不存在或已下架" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/utils/axios';
import { formatDate } from '@/utils/format';
import defaultProductImage from '@/assets/images/default-product.svg';

const route = useRoute();
const router = useRouter();

// 状态
const product = ref(null);
const loading = ref(true);
const error = ref(null);

// 获取商品详情
const fetchProduct = async () => {
  const productId = route.params.id;
  if (!productId) {
    router.push('/shop');
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`/api/shop/products/${productId}/`);
    product.value = response.data;
  } catch (err) {
    console.error('获取商品详情失败:', err);
    error.value = err.response?.data?.detail || '获取商品详情失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};



// 生命周期钩子
onMounted(() => {
  fetchProduct();
});
</script>

<style scoped>
.product-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container,
.error-container,
.empty-container {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.breadcrumb {
  margin-bottom: 20px;
}

.product-content {
  display: flex;
  gap: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.product-image {
  flex: 0 0 400px;
  height: 400px;
  background-color: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 15px;
}

.product-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 20px;
}

.product-price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
  margin-bottom: 20px;
}

.product-description {
  margin-bottom: 30px;
}

.product-description h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #303133;
}

.product-description p {
  color: #606266;
  line-height: 1.6;
  white-space: pre-line;
}



@media (max-width: 768px) {
  .product-content {
    flex-direction: column;
    padding: 15px;
  }
  
  .product-image {
    flex: 0 0 auto;
    height: 250px;
  }
  
  .product-name {
    font-size: 20px;
  }
  
  .product-price {
    font-size: 24px;
  }
}
</style>