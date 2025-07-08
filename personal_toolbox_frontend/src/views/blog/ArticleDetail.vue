<template>
  <div class="article-detail">
    <el-card class="article-card">
      <div class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <el-tag size="small" type="info">{{ article.category?.name }}</el-tag>
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
            {{ article.author?.username }}
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

      <div class="article-content" v-html="renderedContent"></div>

      <div class="article-actions">
        <el-button type="primary" @click="handleLike" :loading="liking">
          <el-icon><Star /></el-icon>
          点赞 {{ article.likes_count }}
        </el-button>
        <el-button 
          type="primary" 
          @click="$router.push(`/blog/edit/${article.id}`)"
          v-if="isAuthor"
        >
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
      </div>
    </el-card>

    <el-card class="comments-card">
      <template #header>
        <div class="card-header">
          <h3>评论 ({{ comments.length }})</h3>
        </div>
      </template>

      <div class="comment-form" v-if="isAuthenticated">
        <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
        />
        <el-button 
          type="primary" 
          @click="submitComment"
          :loading="submitting"
          class="submit-btn"
        >
          发表评论
        </el-button>
      </div>
      <el-alert
        v-else
        title="请先登录后再发表评论"
        type="info"
        :closable="false"
        show-icon
      />

      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-author">{{ comment.author.username }}</span>
            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
          <div class="comment-actions">
            <el-button 
              text 
              size="small" 
              @click="handleCommentLike(comment)"
              :loading="comment.liking"
            >
              <el-icon><Star /></el-icon>
              {{ comment.likes_count }}
            </el-button>
            <el-button 
              text 
              size="small" 
              @click="handleReply(comment)"
              v-if="isAuthenticated"
            >
              回复
            </el-button>
          </div>

          <!-- 嵌套评论 -->
          <div 
            v-for="reply in comment.replies" 
            :key="reply.id" 
            class="reply-item"
          >
            <div class="comment-header">
              <span class="comment-author">{{ reply.author.username }}</span>
              <span class="comment-time">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="comment-content">{{ reply.content }}</div>
            <div class="comment-actions">
              <el-button 
                text 
                size="small" 
                @click="handleCommentLike(reply)"
                :loading="reply.liking"
              >
                <el-icon><Star /></el-icon>
                {{ reply.likes_count }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { User, Calendar, View, Star, Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const { isAuthenticated, userProfile } = userStore

const article = ref({})
const comments = ref([])
const newComment = ref('')
const submitting = ref(false)
const liking = ref(false)

const isAuthor = computed(() => {
  return article.value.author?.id === userProfile?.id
})

const renderedContent = computed(() => {
  return DOMPurify.sanitize(marked(article.value.content || ''))
})

const fetchArticle = async () => {
  try {
    const response = await api.getArticle(route.params.id)
    article.value = response.data
    // 增加浏览次数
    await api.viewArticle(route.params.id)
  } catch (error) {
    ElMessage.error('获取文章详情失败')
    router.push('/blog')
  }
}

const fetchComments = async () => {
  try {
    const response = await api.getComments(route.params.id)
    comments.value = response.data
  } catch (error) {
    ElMessage.error('获取评论列表失败')
  }
}

const handleLike = async () => {
  if (!isAuthenticated) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    liking.value = true
    await api.likeArticle(route.params.id)
    article.value.likes_count++
  } catch (error) {
    ElMessage.error('点赞失败')
  } finally {
    liking.value = false
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  try {
    submitting.value = true
    await api.createComment({
      article: route.params.id,
      content: newComment.value
    })
    newComment.value = ''
    await fetchComments()
    ElMessage.success('评论发表成功')
  } catch (error) {
    ElMessage.error('评论发表失败')
  } finally {
    submitting.value = false
  }
}

const handleCommentLike = async (comment) => {
  if (!isAuthenticated) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    comment.liking = true
    await api.likeComment(comment.id)
    comment.likes_count++
  } catch (error) {
    ElMessage.error('点赞失败')
  } finally {
    comment.liking = false
  }
}

const handleReply = (comment) => {
  newComment.value = `@${comment.author.username} `
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

onMounted(() => {
  fetchArticle()
  fetchComments()
})
</script>

<style scoped>
.article-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.article-card {
  margin-bottom: 20px;
}

.article-header {
  margin-bottom: 30px;
}

.article-title {
  margin: 0 0 20px;
  font-size: 2em;
  color: var(--el-text-color-primary);
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

.article-content {
  line-height: 1.8;
  color: var(--el-text-color-primary);
  margin: 30px 0;
}

.article-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.comment-form {
  margin-bottom: 20px;
}

.submit-btn {
  margin-top: 10px;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: bold;
  color: var(--el-color-primary);
}

.comment-time {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.comment-content {
  line-height: 1.6;
  color: var(--el-text-color-primary);
}

.comment-actions {
  margin-top: 10px;
}

.reply-item {
  margin: 15px 0 15px 20px;
  padding: 15px;
  background-color: var(--el-color-primary-light-9);
  border-radius: 4px;
}
</style>