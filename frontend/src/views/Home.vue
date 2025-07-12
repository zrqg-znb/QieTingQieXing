<template>
  <div class="home-container">
      <!-- 欢迎区域 -->
      <section class="hero-section">
        <div class="hero-content">
          <h1>欢迎来到切听切行</h1>
          <p>集知识库与商城于一体的学习平台</p>
          <div class="hero-buttons">
            <el-button type="primary" size="large" @click="router.push('/wiki')">浏览知识库</el-button>
            <el-button size="large" @click="router.push('/shop')">进入商城</el-button>
          </div>
        </div>
        <div class="hero-image">
          <img src="@/assets/images/welcome.svg" alt="欢迎图片">
        </div>
      </section>

      <!-- 特色功能区域 -->
      <section class="features-section">
        <h2 class="section-title">我们的特色</h2>
        
        <div class="features-grid">
          <div class="feature-card">
            <el-icon class="feature-icon"><Reading /></el-icon>
            <h3>丰富的知识库</h3>
            <p>提供全面的学习资料和教程，帮助您快速掌握各种知识和技能。</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><ShoppingBag /></el-icon>
            <h3>精选商品</h3>
            <p>精心挑选与学习相关的优质商品，满足您的学习和生活需求。</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><User /></el-icon>
            <h3>个性化体验</h3>
            <p>根据您的兴趣和学习历史，提供个性化的内容推荐和购物建议。</p>
          </div>
          
          <div class="feature-card">
            <el-icon class="feature-icon"><Service /></el-icon>
            <h3>专业服务</h3>
            <p>提供专业的客户服务和技术支持，解决您在学习和购物过程中遇到的问题。</p>
          </div>
        </div>
      </section>
      
      <!-- 最新内容区域 -->
      <section class="latest-section">
        <h2 class="section-title">最新内容</h2>
        
        <el-tabs>
          <el-tab-pane label="知识库文章">
            <div class="latest-grid">
              <div v-if="loading && loading.articles" class="loading-placeholder">
                <el-skeleton :rows="3" animated />
              </div>
              
              <div v-else-if="pinnedArticles.length === 0" class="empty-placeholder">
                <el-empty description="暂无最新文章" />
              </div>
              
              <div v-else class="article-list">
                <div 
                  v-for="article in pinnedArticles" 
                  :key="article.id"
                  class="article-card"
                  @click="router.push(`/wiki/article/${article.id}`)"
                >
                  <h3>{{ article.title }}</h3>
                  <p class="article-excerpt">{{ article.excerpt || article.content?.substring(0, 100) + '...' }}</p>
                  <div class="article-meta">
                    <span>{{ article.created_at }}</span>
                    <span>{{ article.category }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="商城商品">
            <div class="latest-grid">
              <div v-if="loading && loading.products" class="loading-placeholder">
                <el-skeleton :rows="3" animated />
              </div>
              
              <div v-else-if="featuredProducts.length === 0" class="empty-placeholder">
                <el-empty description="暂无最新商品" />
              </div>
              
              <div v-else class="product-list">
                <div 
                  v-for="product in featuredProducts" 
                  :key="product.id"
                  class="product-card"
                  @click="router.push(`/shop/product/${product.id}`)"
                >
                  <div class="product-image">
                    <el-image 
                      :src="product.image || defaultProductImage" 
                      fit="cover"
                    />
                  </div>
                  <div class="product-info">
                    <h3>{{ product.name }}</h3>
                    <p class="product-price">¥{{ product.price }}</p>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'
import { Reading, ShoppingBag, User, Service } from '@element-plus/icons-vue'
import defaultProductImage from '@/assets/images/default-product.svg'

// 路由和状态
const router = useRouter()
const userStore = useUserStore()

// 置顶文章和推荐商品
const pinnedArticles = ref([])
const featuredProducts = ref([])
const loading = ref({
  articles: true,
  products: true
})

// 获取置顶文章
async function fetchPinnedArticles() {
  loading.value.articles = true;
  try {
    const response = await axios.get('/api/wiki/articles/', {
      params: {
        is_pinned: true,
        limit: 4
      }
    })
    pinnedArticles.value = response.data.results || []
  } catch (error) {
    console.error('获取置顶文章失败:', error)
  } finally {
    loading.value.articles = false;
  }
}

// 获取推荐商品
async function fetchFeaturedProducts() {
  loading.value.products = true;
  try {
    const response = await axios.get('/api/shop/products/', {
      params: {
        is_active: true,
        limit: 4
      }
    })
    featuredProducts.value = response.data.results || []
  } catch (error) {
    console.error('获取推荐商品失败:', error)
  } finally {
    loading.value.products = false;
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  // 如果用户已登录，获取置顶文章和推荐商品
  if (userStore.isLoggedIn) {
    await Promise.all([
      fetchPinnedArticles(),
      fetchFeaturedProducts()
    ])
  }
})
</script>

<style scoped lang="scss">
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.hero-section {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-bottom: 60px;
  min-height: 400px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    flex: 1;
    
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: var(--el-color-primary);
    }
    
    p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
      color: #606266;
    }
  }
  
  .hero-buttons {
    display: flex;
    gap: 15px;
    
    @media (max-width: 768px) {
      justify-content: center;
    }
  }
  
  .hero-image {
    flex: 1;
    display: flex;
    justify-content: center;
    
    img {
      max-width: 100%;
      max-height: 350px;
    }
  }
}

.section-title {
  text-align: center;
  margin-bottom: 40px;
  font-size: 1.8rem;
  color: #303133;
}

.features-section {
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px 0 rgba(0, 0, 0, 0.15);
  }
  
  h3 {
    margin: 15px 0;
    font-size: 1.2rem;
    color: #303133;
  }
  
  p {
    color: #606266;
    line-height: 1.6;
  }
}

.feature-icon {
  font-size: 2.5rem;
  color: var(--el-color-primary);
}

/* 最新内容区域样式 */
.latest-section {
  margin-bottom: 60px;
}

.latest-grid {
  min-height: 300px;
}

.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.article-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px 0 rgba(0, 0, 0, 0.15);
  }
  
  h3 {
    margin: 0 0 10px;
    font-size: 1.1rem;
    color: #303133;
  }
}

.article-excerpt {
  color: #606266;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 0.9rem;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px 0 rgba(0, 0, 0, 0.15);
  }
  
  .product-image {
    height: 180px;
    overflow: hidden;
    
    .el-image {
      width: 100%;
      height: 100%;
    }
  }
  
  .product-info {
    padding: 15px;
    
    h3 {
      margin: 0 0 10px;
      font-size: 1.1rem;
      color: #303133;
    }
    
    .product-price {
      color: #f56c6c;
      font-weight: bold;
      margin: 0;
    }
  }
}

.loading-placeholder,
.empty-placeholder {
  padding: 30px;
}

</style>