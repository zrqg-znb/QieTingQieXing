<template>
  <div class="article-editor">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑文章' : '写文章' }}</h2>
        </div>
      </template>

      <el-form :model="articleForm" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="articleForm.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="分类" prop="category_id">
          <el-select v-model="articleForm.category_id" placeholder="选择分类">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
          <el-button 
            type="primary" 
            link 
            @click="showCategoryDialog = true"
          >
            新建分类
          </el-button>
        </el-form-item>

        <el-form-item label="标签" prop="tag_ids">
          <el-select
            v-model="articleForm.tag_ids"
            multiple
            placeholder="选择标签"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
          <el-button 
            type="primary" 
            link 
            @click="showTagDialog = true"
          >
            新建标签
          </el-button>
        </el-form-item>

        <el-form-item label="封面" prop="cover">
          <el-upload
            class="cover-uploader"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :before-upload="beforeCoverUpload"
          >
            <img v-if="articleForm.cover" :src="articleForm.cover" class="cover" />
            <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="articleForm.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <div class="editor-container">
            <div class="editor-toolbar">
              <el-button-group>
                <el-button @click="insertText('**', '**')">粗体</el-button>
                <el-button @click="insertText('*', '*')">斜体</el-button>
                <el-button @click="insertText('# ')">标题</el-button>
                <el-button @click="insertText('- ')">列表</el-button>
                <el-button @click="insertText('[', '](url)')">链接</el-button>
                <el-button @click="insertText('![alt](', ')')">图片</el-button>
                <el-button @click="insertText('```\n', '\n```')">代码块</el-button>
              </el-button-group>
            </div>
            <el-input
              v-model="articleForm.content"
              type="textarea"
              :rows="15"
              placeholder="使用Markdown编写文章内容"
            />
          </div>
          <div class="preview-container">
            <div class="preview-header">
              <h3>预览</h3>
            </div>
            <div class="markdown-preview" v-html="renderedContent"></div>
          </div>
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="articleForm.status">
            <el-radio :label="'draft'">草稿</el-radio>
            <el-radio :label="'published'">发布</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            {{ isEdit ? '更新' : '发布' }}
          </el-button>
          <el-button @click="$router.push('/blog')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 新建分类对话框 -->
    <el-dialog
      v-model="showCategoryDialog"
      title="新建分类"
      width="30%"
    >
      <el-form :model="newCategory" :rules="categoryRules" ref="categoryFormRef">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="newCategory.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCategoryDialog = false">取消</el-button>
          <el-button type="primary" @click="createCategory" :loading="creatingCategory">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 新建标签对话框 -->
    <el-dialog
      v-model="showTagDialog"
      title="新建标签"
      width="30%"
    >
      <el-form :model="newTag" :rules="tagRules" ref="tagFormRef">
        <el-form-item label="标签名称" prop="name">
          <el-input v-model="newTag.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showTagDialog = false">取消</el-button>
          <el-button type="primary" @click="createTag" :loading="creatingTag">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const categoryFormRef = ref(null)
const tagFormRef = ref(null)

const isEdit = computed(() => route.params.id)

const articleForm = ref({
  title: '',
  category_id: '',
  tag_ids: [],
  cover: '',
  summary: '',
  content: '',
  status: 'draft'
})

const categories = ref([])
const tags = ref([])
const submitting = ref(false)

const showCategoryDialog = ref(false)
const showTagDialog = ref(false)
const newCategory = ref({ name: '' })
const newTag = ref({ name: '' })
const creatingCategory = ref(false)
const creatingTag = ref(false)

const rules = {
  title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择文章分类', trigger: 'change' }],
  content: [{ required: true, message: '请输入文章内容', trigger: 'blur' }]
}

const categoryRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

const tagRules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

const renderedContent = computed(() => {
  return DOMPurify.sanitize(marked(articleForm.value.content || ''))
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

const fetchArticle = async () => {
  if (!isEdit.value) return
  try {
    const response = await api.getArticle(route.params.id)
    const article = response.data
    articleForm.value = {
      title: article.title,
      category_id: article.category.id,
      tag_ids: article.tags.map(tag => tag.id),
      cover: article.cover,
      summary: article.summary,
      content: article.content,
      status: article.status
    }
  } catch (error) {
    ElMessage.error('获取文章详情失败')
    router.push('/blog')
  }
}

const createCategory = async () => {
  if (!categoryFormRef.value) return
  await categoryFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        creatingCategory.value = true
        const response = await api.createCategory(newCategory.value)
        categories.value.push(response.data)
        showCategoryDialog.value = false
        newCategory.value.name = ''
        ElMessage.success('分类创建成功')
      } catch (error) {
        ElMessage.error('分类创建失败')
      } finally {
        creatingCategory.value = false
      }
    }
  })
}

const createTag = async () => {
  if (!tagFormRef.value) return
  await tagFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        creatingTag.value = true
        const response = await api.createTag(newTag.value)
        tags.value.push(response.data)
        showTagDialog.value = false
        newTag.value.name = ''
        ElMessage.success('标签创建成功')
      } catch (error) {
        ElMessage.error('标签创建失败')
      } finally {
        creatingTag.value = false
      }
    }
  })
}

const beforeCoverUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
  }
  return isImage && isLt2M
}

const handleCoverSuccess = (response) => {
  articleForm.value.cover = response.url
}

const insertText = (prefix, suffix = '') => {
  const textarea = document.querySelector('.editor-container textarea')
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = articleForm.value.content
  const selectedText = text.substring(start, end)
  
  articleForm.value.content = 
    text.substring(0, start) +
    prefix +
    selectedText +
    suffix +
    text.substring(end)

  // 恢复光标位置
  setTimeout(() => {
    textarea.focus()
    textarea.setSelectionRange(
      start + prefix.length,
      end + prefix.length
    )
  })
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        if (isEdit.value) {
          await api.updateArticle(route.params.id, articleForm.value)
          ElMessage.success('文章更新成功')
        } else {
          await api.createArticle(articleForm.value)
          ElMessage.success('文章发布成功')
        }
        router.push('/blog')
      } catch (error) {
        ElMessage.error(isEdit.value ? '文章更新失败' : '文章发布失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchArticle()
})
</script>

<style scoped>
.article-editor {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.editor-container {
  margin-bottom: 20px;
}

.editor-toolbar {
  margin-bottom: 10px;
}

.preview-container {
  margin-top: 20px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
}

.preview-header {
  padding: 10px;
  border-bottom: 1px solid var(--el-border-color);
  background-color: var(--el-color-primary-light-9);
}

.preview-header h3 {
  margin: 0;
}

.markdown-preview {
  padding: 20px;
  min-height: 200px;
}

.cover-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration);
}

.cover-uploader:hover {
  border-color: var(--el-color-primary);
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.cover {
  width: 178px;
  height: 178px;
  display: block;
}
</style>