<template>
  <div class="product-card" @click="navigateToDetail">
    <div class="product-image">
      <el-image 
        :src="product.image || defaultProductImage" 
        :alt="product.name"
        fit="cover"
      />
    </div>
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-description">{{ truncatedDescription }}</p>
      <div class="product-footer">
        <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { truncateText } from '@/utils/format';
import defaultProductImage from '@/assets/images/default-product.svg';

const router = useRouter();

// 定义组件属性
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

// 计算属性：截断的商品描述
const truncatedDescription = computed(() => {
  return truncateText(props.product.description || '', 50);
});

// 导航到商品详情页
const navigateToDetail = () => {
  router.push(`/shop/product/${props.product.id}`);
};


</script>

<style scoped>
.product-card {
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  cursor: pointer;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.product-image {
  height: 200px;
  overflow: hidden;
  background-color: #f5f7fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-info {
  padding: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.product-price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

@media (max-width: 768px) {
  .product-image {
    height: 150px;
  }
  
  .product-info {
    padding: 10px;
  }
  
  .product-name {
    font-size: 14px;
  }
  
  .product-description {
    font-size: 12px;
    margin-bottom: 10px;
  }
  
  .product-price {
    font-size: 16px;
  }
}
</style>