<template>
  <div class="article-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="15" animated />
    </div>
    
    <!-- 文章内容 -->
    <template v-else-if="article">
      <el-card class="article-card">
        <div class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>
          
          <div class="article-meta">
            <div class="meta-left">
              <span class="meta-item">
                <el-avatar :size="30" :src="article.author.avatar">
                  {{ article.author.nickname?.charAt(0) || article.author.username?.charAt(0) || 'U' }}
                </el-avatar>
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
            
            <div class="meta-right" v-if="canEdit">
              <el-button type="primary" size="small" @click="handleEdit">
                编辑
              </el-button>
            </div>
          </div>
          
          <div class="article-tags">
            <el-tag 
              v-for="tag in article.tags" 
              :key="tag.id"
              effect="plain"
              class="article-tag"
              @click="navigateToTag(tag.id)"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>
        
        <el-divider />
        
        <div class="article-content" v-html="article.content"></div>
        
        <div class="article-actions">
          <el-button 
            type="primary" 
            :icon="Star" 
            circle 
            :class="{ 'is-liked': isLiked }"
            @click="handleLike"
          />
        </div>
        
        <!-- 附件列表 -->
        <div v-if="article.attachments && article.attachments.length > 0" class="attachments-section">
          <h3>附件</h3>
          <el-table :data="article.attachments" style="width: 100%">
            <el-table-column prop="name" label="文件名">
              <template #default="{ row }">
                <el-link type="primary" @click="downloadAttachment(row)">
                  {{ row.name }}
                </el-link>
              </template>
            </el-table-column>
            <el-table-column prop="file_type" label="类型" width="120" />
            <el-table-column prop="file_size" label="大小" width="120">
              <template #default="{ row }">
                {{ formatFileSize(row.file_size) }}
              </template>
            </el-table-column>
            <el-table-column prop="download_count" label="下载次数" width="120" />
          </el-table>
        </div>
      </el-card>
      
      <!-- 评论区 -->
      <el-card class="comments-card">
        <template #header>
          <div class="comments-header">
            <h3>评论 ({{ article.comments?.length || 0 }})</h3>
          </div>
        </template>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <template v-if="article.comments && article.comments.length > 0">
            <div 
              v-for="comment in article.comments" 
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-avatar">
                <el-avatar :size="40" :src="comment.author.avatar">
                  {{ comment.author.nickname?.charAt(0) || comment.author.username?.charAt(0) || 'U' }}
                </el-avatar>
              </div>
              
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.author.nickname || comment.author.username }}</span>
                  <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                </div>
                
                <div class="comment-text">{{ comment.content }}</div>
                
                <div class="comment-actions">
                  <el-button text type="primary" @click="showReplyForm(comment.id)">
                    回复
                  </el-button>
                  
                  <el-button 
                    v-if="canDeleteComment(comment)" 
                    text 
                    type="danger" 
                    @click="handleDeleteComment(comment.id)"
                  >
                    删除
                  </el-button>
                </div>
                
                <!-- 回复表单 -->
                <div v-if="replyToCommentId === comment.id" class="reply-form">
                  <el-input
                    v-model="replyContent"
                    type="textarea"
                    :rows="2"
                    placeholder="写下你的回复..."
                  />
                  <div class="reply-actions">
                    <el-button @click="cancelReply">取消</el-button>
                    <el-button type="primary" @click="submitReply(comment.id)" :loading="submittingReply">
                      提交回复
                    </el-button>
                  </div>
                </div>
                
                <!-- 回复列表 -->
                <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
                  <div 
                    v-for="reply in comment.replies" 
                    :key="reply.id"
                    class="reply-item"
                  >
                    <div class="reply-avatar">
                      <el-avatar :size="30" :src="reply.author.avatar">
                        {{ reply.author.nickname?.charAt(0) || reply.author.username?.charAt(0) || 'U' }}
                      </el-avatar>
                    </div>
                    
                    <div class="reply-content">
                      <div class="reply-header">
                        <span class="reply-author">{{ reply.author.nickname || reply.author.username }}</span>
                        <span class="reply-time">{{ formatDate(reply.created_at) }}</span>
                      </div>
                      
                      <div class="reply-text">{{ reply.content }}</div>
                      
                      <div class="reply-actions">
                        <el-button 
                          v-if="canDeleteComment(reply)" 
                          text 
                          type="danger" 
                          @click="handleDeleteComment(reply.id)"
                        >
                          删除
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
          
          <div v-else class="no-comments">
            暂无评论，快来发表第一条评论吧！
          </div>
        </div>
        
        <!-- 评论表单 -->
        <div v-if="userStore.isLoggedIn" class="comment-form">
          <h4>发表评论</h4>
          <el-input
            v-model="commentContent"
            type="textarea"
            :rows="4"
            placeholder="写下你的评论..."
          />
          <div class="form-actions">
            <el-button type="primary" @click="submitComment" :loading="submittingComment">
              提交评论
            </el-button>
          </div>
        </div>
        
        <div v-else class="login-to-comment">
          <el-alert
            title="请登录后发表评论"
            type="info"
            :closable="false"
            center
            show-icon
          >
            <template #default>
              <el-button type="primary" @click="navigateToLogin">去登录</el-button>
            </template>
          </el-alert>
        </div>
      </el-card>
    </template>
    
    <!-- 文章不存在 -->
    <el-empty v-else description="文章不存在或已被删除" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, View, Star } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'
import { formatDate } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 文章ID
const articleId = computed(() => route.params.id)

// 加载状态
const loading = ref(true)

// 文章数据
const article = ref(null)

// 评论相关
const commentContent = ref('')
const replyContent = ref('')
const replyToCommentId = ref(null)
const submittingComment = ref(false)
const submittingReply = ref(false)

// 点赞状态
const isLiked = ref(false)

// 获取文章详情
async function fetchArticle() {
  try {
    loading.value = true
    
    const response = await axios.get(`/api/wiki/articles/${articleId.value}/`)
    article.value = response.data
    
    // 检查是否已点赞
    checkLikeStatus()
  } catch (error) {
    console.error('获取文章详情失败:', error)
    ElMessage.error('获取文章详情失败')
  } finally {
    loading.value = false
  }
}

// 检查点赞状态
async function checkLikeStatus() {
  if (!userStore.isLoggedIn) return
  
  try {
    const response = await axios.get(`/api/wiki/articles/${articleId.value}/like-status/`)
    isLiked.value = response.data.is_liked
  } catch (error) {
    console.error('获取点赞状态失败:', error)
  }
}

// 处理点赞
async function handleLike() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    await axios.post(`/api/wiki/articles/${articleId.value}/like/`)
    
    // 更新点赞状态和数量
    isLiked.value = !isLiked.value
    if (isLiked.value) {
      article.value.likes += 1
    } else {
      article.value.likes -= 1
    }
  } catch (error) {
    console.error('点赞操作失败:', error)
    ElMessage.error('点赞操作失败')
  }
}

// 提交评论
async function submitComment() {
  if (!commentContent.value.trim()) {
    ElMessage.warning('评论内容不能为空')
    return
  }
  
  try {
    submittingComment.value = true
    
    const response = await axios.post('/api/wiki/comments/', {
      article: articleId.value,
      content: commentContent.value
    })
    
    // 添加新评论到列表
    if (!article.value.comments) {
      article.value.comments = []
    }
    
    article.value.comments.unshift(response.data)
    
    // 清空评论内容
    commentContent.value = ''
    
    ElMessage.success('评论发表成功')
  } catch (error) {
    console.error('发表评论失败:', error)
    ElMessage.error('发表评论失败')
  } finally {
    submittingComment.value = false
  }
}

// 显示回复表单
function showReplyForm(commentId) {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  replyToCommentId.value = commentId
  replyContent.value = ''
}

// 取消回复
function cancelReply() {
  replyToCommentId.value = null
  replyContent.value = ''
}

// 提交回复
async function submitReply(commentId) {
  if (!replyContent.value.trim()) {
    ElMessage.warning('回复内容不能为空')
    return
  }
  
  try {
    submittingReply.value = true
    
    const response = await axios.post('/api/wiki/comments/', {
      article: articleId.value,
      content: replyContent.value,
      parent: commentId
    })
    
    // 添加新回复到列表
    const parentComment = article.value.comments.find(c => c.id === commentId)
    if (parentComment) {
      if (!parentComment.replies) {
        parentComment.replies = []
      }
      parentComment.replies.push(response.data)
    }
    
    // 清空回复内容并隐藏回复表单
    cancelReply()
    
    ElMessage.success('回复发表成功')
  } catch (error) {
    console.error('发表回复失败:', error)
    ElMessage.error('发表回复失败')
  } finally {
    submittingReply.value = false
  }
}

// 删除评论
async function handleDeleteComment(commentId) {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/wiki/comments/${commentId}/`)
    
    // 从列表中移除评论
    const commentIndex = article.value.comments.findIndex(c => c.id === commentId)
    if (commentIndex !== -1) {
      article.value.comments.splice(commentIndex, 1)
    } else {
      // 可能是回复，查找并移除
      article.value.comments.forEach(comment => {
        if (comment.replies) {
          const replyIndex = comment.replies.findIndex(r => r.id === commentId)
          if (replyIndex !== -1) {
            comment.replies.splice(replyIndex, 1)
          }
        }
      })
    }
    
    ElMessage.success('评论删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error)
      ElMessage.error('删除评论失败')
    }
  }
}

// 下载附件
async function downloadAttachment(attachment) {
  try {
    const response = await axios.get(`/api/wiki/attachments/${attachment.id}/download/`, {
      responseType: 'blob'
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', attachment.name)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // 更新下载次数
    attachment.download_count += 1
  } catch (error) {
    console.error('下载附件失败:', error)
    ElMessage.error('下载附件失败')
  }
}

// 导航到标签页面
function navigateToTag(tagId) {
  router.push({
    path: '/wiki',
    query: { tag: tagId }
  })
}

// 导航到登录页面
function navigateToLogin() {
  router.push('/login')
}

// 处理编辑文章
function handleEdit() {
  router.push(`/wiki/edit/${articleId.value}`)
}

// 格式化文件大小
function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 检查是否可以编辑文章
const canEdit = computed(() => {
  if (!userStore.isLoggedIn || !article.value) return false
  
  // 管理员或文章作者可以编辑
  return userStore.user.is_staff || userStore.user.id === article.value.author.id
})

// 检查是否可以删除评论
function canDeleteComment(comment) {
  if (!userStore.isLoggedIn) return false
  
  // 管理员或评论作者可以删除
  return userStore.user.is_staff || userStore.user.id === comment.author.id
}

// 组件挂载时获取文章详情
onMounted(() => {
  fetchArticle()
})
</script>

<style scoped lang="scss">
.article-container {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.loading-container {
  padding: 20px 0;
}

.article-card {
  margin-bottom: 20px;
}

.article-header {
  margin-bottom: 20px;
  
  .article-title {
    font-size: 28px;
    margin-bottom: 15px;
  }
  
  .article-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    
    .meta-left {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      align-items: center;
    }
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #606266;
      font-size: 14px;
    }
  }
  
  .article-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    
    .article-tag {
      cursor: pointer;
    }
  }
}

.article-content {
  line-height: 1.8;
  font-size: 16px;
  color: #303133;
  
  :deep(h1, h2, h3, h4, h5, h6) {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
  }
  
  :deep(p) {
    margin-bottom: 1em;
  }
  
  :deep(img) {
    max-width: 100%;
    height: auto;
  }
  
  :deep(pre) {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
  }
  
  :deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 1em 0;
  }
  
  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1em;
    
    th, td {
      border: 1px solid #EBEEF5;
      padding: 8px 12px;
    }
    
    th {
      background-color: #F5F7FA;
    }
  }
}

.article-actions {
  display: flex;
  justify-content: center;
  margin: 30px 0;
  
  .is-liked {
    background-color: #F56C6C;
    border-color: #F56C6C;
  }
}

.attachments-section {
  margin-top: 30px;
  
  h3 {
    font-size: 18px;
    margin-bottom: 15px;
  }
}

.comments-card {
  margin-bottom: 20px;
}

.comments-header {
  h3 {
    margin: 0;
    font-size: 18px;
  }
}

.comments-list {
  margin-bottom: 30px;
}

.comment-item {
  display: flex;
  margin-bottom: 20px;
  
  .comment-avatar {
    margin-right: 15px;
  }
  
  .comment-content {
    flex: 1;
  }
  
  .comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
    
    .comment-author {
      font-weight: bold;
      color: #303133;
    }
    
    .comment-time {
      font-size: 12px;
      color: #909399;
    }
  }
  
  .comment-text {
    margin-bottom: 10px;
    line-height: 1.6;
  }
  
  .comment-actions {
    display: flex;
    gap: 10px;
  }
}

.reply-form {
  margin: 10px 0;
  
  .reply-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
    gap: 10px;
  }
}

.replies-list {
  margin-top: 15px;
  margin-left: 20px;
  border-left: 2px solid #EBEEF5;
  padding-left: 15px;
}

.reply-item {
  display: flex;
  margin-bottom: 15px;
  
  .reply-avatar {
    margin-right: 10px;
  }
  
  .reply-content {
    flex: 1;
  }
  
  .reply-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
    
    .reply-author {
      font-weight: bold;
      color: #303133;
    }
    
    .reply-time {
      font-size: 12px;
      color: #909399;
    }
  }
  
  .reply-text {
    margin-bottom: 5px;
    line-height: 1.6;
  }
  
  .reply-actions {
    display: flex;
    gap: 10px;
  }
}

.no-comments {
  text-align: center;
  color: #909399;
  padding: 20px 0;
}

.comment-form {
  h4 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
  }
}

.login-to-comment {
  margin-top: 20px;
}
</style>