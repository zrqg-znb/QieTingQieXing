<template>
  <div class="article-list">
    <div class="page-header">
      <h1>博客文章</h1>
      <el-button type="primary" @click="$router.push('/blog/new')" v-if="isAuthenticated">
        <el-icon><Plus /></el-icon>写文章
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="filter-card">
          <template #header>
            <div class="card-header">
              <h3>筛选</h3>
            </div>
          </template>
          
          <el-form>
            <el-form-item label="分类">
              <el-select v-model="filters.category" clearable placeholder="选择分类">
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="标签">
              <el-select v-model="filters.tag" clearable placeholder="选择标签">
                <el-option
                  v-for="tag in tags"
                  :key="tag.id"
                  :label="tag.name"
                  :value="tag.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="作者">
              <el-input
                v-model="filters.author"
                placeholder="作者名称"
                clearable
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="18">
        <el-card v-for="article in articles" :key="article.id" class="article-card">
          <div class="article-header">
            <h2 class="article-title" @click="$router.push(`/blog/article/${article.id}`)">
              {{ article.title }}
            </h2>
            <div class="article-meta">
              <el-tag size="small" type="info">{{ article.category.name }}</el-tag>
              <el-tag
                v-for="tag in article.tags"
                :key="tag.id"
                size="small"
                class="mx-1"
              >
                {{ tag.name }}
              </el-tag>
              <span class="meta-item">
                <el-icon><User /></el-icon>
                {{ article.author.username }}
              </span>
              <span class="meta-item">
                <el-icon><Calendar /></el-icon>
                {{ formatDate(article.created_at) }}
              </span>
              <span class="meta-item">
                <el-icon><View /></el-icon>
                {{ article.views_count }}
              </span>
              <span class="meta-item">
                <el-icon><Star /></el-icon>
                {{ article.likes_count }}
              </span>
            </div>
          </div>

          <p class="article-summary">{{ article.summary }}</p>

          <div class="article-footer">
            <el-button text @click="$router.push(`/blog/article/${article.id}`)">
              阅读全文
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </el-card>

        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Plus, User, Calendar, View, Star, ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import api from '@/api'

const userStore = useUserStore()
const { isAuthenticated } = userStore

const articles = ref([])
const categories = ref([])
const tags = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filters = ref({
  category: '',
  tag: '',
  author: ''
})

const fetchCategories = async () => {
  try {
    const response = await api.getCategories()
    categories.value = response.data
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

const fetchTags = async () => {
  try {
    const response = await api.getTags()
    tags.value = response.data
  } catch (error) {
    ElMessage.error('获取标签列表失败')
  }
}

const fetchArticles = async () => {
  try {
    const response = await api.getArticles({
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters.value
    })
    articles.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    ElMessage.error('获取文章列表失败')
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchArticles()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchArticles()
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

watch(filters, () => {
  currentPage.value = 1
  fetchArticles()
}, { deep: true })

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchArticles()
})
</script>

<style scoped>
.article-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.article-card {
  margin-bottom: 20px;
}

.article-header {
  margin-bottom: 15px;
}

.article-title {
  margin: 0 0 10px;
  cursor: pointer;
  color: var(--el-color-primary);
}

.article-title:hover {
  color: var(--el-color-primary-light-3);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.article-summary {
  color: var(--el-text-color-regular);
  margin: 15px 0;
  line-height: 1.6;
}

.article-footer {
  display: flex;
  justify-content: flex-end;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>