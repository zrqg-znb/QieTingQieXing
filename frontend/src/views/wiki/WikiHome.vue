<template>
  <div class="wiki-container">
    <el-row :gutter="20">
      <!-- 侧边栏 -->
      <el-col :xs="24" :sm="6" :md="5" :lg="4">
        <el-card class="sidebar-card">
          <template #header>
            <div class="sidebar-header">
              <h3>知识库分类</h3>
              <el-button v-if="userStore.isLoggedIn" type="primary" size="small" @click="navigateToCreate">
                发布文章
              </el-button>
            </div>
          </template>
          
          <div class="sidebar-content">
            <el-menu
              :default-active="activeCategory"
              class="category-menu"
              @select="handleCategorySelect"
            >
              <el-menu-item index="all">
                <el-icon><Document /></el-icon>
                <span>全部文章</span>
              </el-menu-item>
              
              <el-menu-item 
                v-for="category in categories" 
                :key="category.id"
                :index="category.id.toString()"
              >
                <el-icon><Folder /></el-icon>
                <span>{{ category.name }}</span>
              </el-menu-item>
            </el-menu>
            
            <div class="tag-section">
              <h4>热门标签</h4>
              <div class="tag-cloud">
                <el-tag
                  v-for="tag in tags"
                  :key="tag.id"
                  :type="activeTag === tag.id.toString() ? '' : 'info'"
                  effect="plain"
                  class="tag-item"
                  @click="handleTagSelect(tag.id.toString())"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 主内容区 -->
      <el-col :xs="24" :sm="18" :md="19" :lg="20">
        <el-card class="main-card">
          <template #header>
            <div class="main-header">
              <h2>{{ getHeaderTitle() }}</h2>
              <div class="search-box">
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索文章"
                  clearable
                  @keyup.enter="handleSearch"
                >
                  <template #append>
                    <el-button @click="handleSearch">
                      <el-icon><Search /></el-icon>
                    </el-button>
                  </template>
                </el-input>
              </div>
            </div>
          </template>
          
          <div class="main-content">
            <!-- 加载状态 -->
            <div v-if="loading" class="loading-container">
              <el-skeleton :rows="10" animated />
            </div>
            
            <!-- 文章列表 -->
            <div v-else-if="articles.length > 0" class="article-list">
              <el-card 
                v-for="article in articles" 
                :key="article.id"
                class="article-card"
                shadow="hover"
                @click="navigateToArticle(article.id)"
              >
                <div class="article-header">
                  <h3 class="article-title">
                    <el-tag v-if="article.is_pinned" type="danger" effect="dark" size="small" class="pin-tag">
                      置顶
                    </el-tag>
                    {{ article.title }}
                  </h3>
                  <div class="article-meta">
                    <span class="meta-item">
                      <el-icon><User /></el-icon>
                      {{ article.author.nickname || article.author.username }}
                    </span>
                    <span class="meta-item">
                      <el-icon><Calendar /></el-icon>
                      {{ formatDate(article.created_at) }}
                    </span>
                    <span class="meta-item">
                      <el-icon><View /></el-icon>
                      {{ article.views }} 浏览
                    </span>
                    <span class="meta-item">
                      <el-icon><Star /></el-icon>
                      {{ article.likes }} 点赞
                    </span>
                  </div>
                </div>
                
                <div class="article-summary">
                  {{ article.summary || truncateContent(article.content) }}
                </div>
                
                <div class="article-footer">
                  <div class="article-tags">
                    <el-tag 
                      v-for="tag in article.tags" 
                      :key="tag.id"
                      size="small"
                      effect="plain"
                      class="article-tag"
                    >
                      {{ tag.name }}
                    </el-tag>
                  </div>
                  <el-button text type="primary">阅读全文</el-button>
                </div>
              </el-card>
              
              <!-- 分页 -->
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="[10, 20, 30, 50]"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="totalArticles"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                />
              </div>
            </div>
            
            <!-- 无数据状态 -->
            <div v-else class="empty-state">
              <el-empty description="暂无文章" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Document, Folder, User, Calendar, View, Star, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'
import { formatDate } from '@/utils/format'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 加载状态
const loading = ref(true)

// 分类和标签
const categories = ref([])
const tags = ref([])

// 文章列表
const articles = ref([])
const totalArticles = ref(0)

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选参数
const activeCategory = ref('all')
const activeTag = ref('')
const searchQuery = ref('')

// 获取分类列表
async function fetchCategories() {
  try {
    const response = await axios.get('/api/wiki/categories/')
    categories.value = response.data.results || []
  } catch (error) {
    console.error('获取分类列表失败:', error)
    ElMessage.error('获取分类列表失败')
  }
}

// 获取标签列表
async function fetchTags() {
  try {
    const response = await axios.get('/api/wiki/tags/')
    tags.value = response.data.results || []
  } catch (error) {
    console.error('获取标签列表失败:', error)
    ElMessage.error('获取标签列表失败')
  }
}

// 获取文章列表
async function fetchArticles() {
  try {
    loading.value = true
    
    // 构建查询参数
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    // 添加分类筛选
    if (activeCategory.value && activeCategory.value !== 'all') {
      params.category = activeCategory.value
    }
    
    // 添加标签筛选
    if (activeTag.value) {
      params.tag = activeTag.value
    }
    
    // 添加搜索筛选
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    const response = await axios.get('/api/wiki/articles/', { params })
    
    articles.value = response.data.results || []
    totalArticles.value = response.data.count || 0
  } catch (error) {
    console.error('获取文章列表失败:', error)
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

// 处理分类选择
function handleCategorySelect(categoryId) {
  activeCategory.value = categoryId
  activeTag.value = ''
  currentPage.value = 1
  fetchArticles()
}

// 处理标签选择
function handleTagSelect(tagId) {
  if (activeTag.value === tagId) {
    // 如果点击的是当前选中的标签，则取消选择
    activeTag.value = ''
  } else {
    activeTag.value = tagId
  }
  currentPage.value = 1
  fetchArticles()
}

// 处理搜索
function handleSearch() {
  currentPage.value = 1
  fetchArticles()
}

// 处理页码变化
function handleCurrentChange(page) {
  currentPage.value = page
  fetchArticles()
}

// 处理每页条数变化
function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1
  fetchArticles()
}

// 导航到文章详情页
function navigateToArticle(articleId) {
  router.push(`/wiki/article/${articleId}`)
}

// 导航到创建文章页面
function navigateToCreate() {
  router.push('/wiki/create')
}

// 获取头部标题
function getHeaderTitle() {
  if (searchQuery.value) {
    return `搜索: ${searchQuery.value}`
  }
  
  if (activeTag.value) {
    const selectedTag = tags.value.find(tag => tag.id.toString() === activeTag.value)
    return selectedTag ? `标签: ${selectedTag.name}` : '知识库'
  }
  
  if (activeCategory.value === 'all') {
    return '全部文章'
  }
  
  const selectedCategory = categories.value.find(category => category.id.toString() === activeCategory.value)
  return selectedCategory ? selectedCategory.name : '知识库'
}

// 截断内容
function truncateContent(content) {
  if (!content) return ''
  
  // 移除HTML标签
  const plainText = content.replace(/<[^>]+>/g, '')
  
  // 截断文本
  return plainText.length > 150 ? plainText.substring(0, 150) + '...' : plainText
}

// 监听路由变化
watch(
  () => route.query,
  (newQuery) => {
    // 从路由参数中获取筛选条件
    if (newQuery.category) {
      activeCategory.value = newQuery.category
    }
    
    if (newQuery.tag) {
      activeTag.value = newQuery.tag
    }
    
    if (newQuery.search) {
      searchQuery.value = newQuery.search
    }
    
    fetchArticles()
  },
  { immediate: true }
)

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchCategories(),
    fetchTags()
  ])
  
  fetchArticles()
})
</script>

<style scoped lang="scss">
.wiki-container {
  padding: 20px;
}

.sidebar-card,
.main-card {
  margin-bottom: 20px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h3 {
    margin: 0;
    font-size: 16px;
  }
}

.category-menu {
  border-right: none;
  margin-bottom: 20px;
}

.tag-section {
  h4 {
    font-size: 14px;
    margin-bottom: 10px;
  }
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  
  .tag-item {
    cursor: pointer;
  }
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  
  h2 {
    margin: 0;
    font-size: 18px;
  }
  
  .search-box {
    width: 300px;
    max-width: 100%;
  }
}

.loading-container {
  padding: 20px 0;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  cursor: pointer;
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-5px);
  }
}

.article-header {
  margin-bottom: 10px;
  
  .article-title {
    margin: 0 0 10px 0;
    font-size: 18px;
    display: flex;
    align-items: center;
    
    .pin-tag {
      margin-right: 8px;
    }
  }
  
  .article-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    color: #909399;
    font-size: 13px;
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
}

.article-summary {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.6;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .article-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.empty-state {
  padding: 40px 0;
  display: flex;
  justify-content: center;
}
</style>