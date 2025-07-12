<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
        </div>
      </template>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="6" animated />
      </div>
      
      <div v-else>
        <el-tabs v-model="activeTab">
          <!-- 个人信息标签页 -->
          <el-tab-pane label="个人信息" name="info">
            <div class="avatar-container">
              <el-avatar :size="100" :src="userInfo.avatar || defaultAvatar">
                {{ userInfo.nickname?.charAt(0) || userInfo.username?.charAt(0) || 'U' }}
              </el-avatar>
              <el-upload
                class="avatar-uploader"
                action="/api/authority/users/upload-avatar/"
                :headers="uploadHeaders"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <el-button size="small" type="primary">更换头像</el-button>
              </el-upload>
            </div>
            
            <el-form
              ref="profileFormRef"
              :model="profileForm"
              :rules="profileRules"
              label-width="100px"
              class="profile-form"
            >
              <el-form-item label="用户名">
                <el-input v-model="userInfo.username" disabled />
              </el-form-item>
              
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="profileForm.nickname" />
              </el-form-item>
              
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="profileForm.email" />
              </el-form-item>
              
              <el-form-item label="手机号码" prop="phone">
                <el-input v-model="profileForm.phone" />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="updateProfile" :loading="updating">
                  保存修改
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <!-- 修改密码标签页 -->
          <el-tab-pane label="修改密码" name="password">
            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="120px"
              class="password-form"
            >
              <el-form-item label="当前密码" prop="old_password">
                <el-input 
                  v-model="passwordForm.old_password" 
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="新密码" prop="new_password">
                <el-input 
                  v-model="passwordForm.new_password" 
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="确认新密码" prop="confirm_password">
                <el-input 
                  v-model="passwordForm.confirm_password" 
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="changePassword" :loading="changingPassword">
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

// 默认头像
const defaultAvatar = '/src/assets/images/default-avatar.svg'

// 用户状态管理
const userStore = useUserStore()

// 当前激活的标签页
const activeTab = ref('info')

// 加载状态
const loading = ref(true)
const updating = ref(false)
const changingPassword = ref(false)

// 用户信息
const userInfo = ref({
  username: '',
  nickname: '',
  email: '',
  phone: '',
  avatar: ''
})

// 个人资料表单
const profileFormRef = ref(null)
const profileForm = reactive({
  nickname: '',
  email: '',
  phone: ''
})

// 密码表单
const passwordFormRef = ref(null)
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 上传头像的请求头
const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${userStore.token}`
  }
})

// 验证新密码确认
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 个人资料表单验证规则
const profileRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度应为2-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 密码表单验证规则
const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 获取用户信息
async function fetchUserProfile() {
  try {
    loading.value = true
    await userStore.fetchUserProfile()
    
    // 更新本地用户信息
    userInfo.value = { ...userStore.user }
    
    // 更新表单数据
    profileForm.nickname = userInfo.value.nickname || ''
    profileForm.email = userInfo.value.email || ''
    profileForm.phone = userInfo.value.phone || ''
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 更新个人资料
async function updateProfile() {
  if (!profileFormRef.value) return
  
  try {
    // 表单验证
    await profileFormRef.value.validate()
    
    // 设置更新状态
    updating.value = true
    
    // 调用更新接口
    await userStore.updateUserProfile({
      nickname: profileForm.nickname,
      email: profileForm.email,
      phone: profileForm.phone
    })
    
    // 更新成功提示
    ElMessage.success('个人资料更新成功')
    
    // 重新获取用户信息
    await fetchUserProfile()
  } catch (error) {
    console.error('更新个人资料失败:', error)
    
    // 显示错误信息
    if (error.response && error.response.data) {
      const errorData = error.response.data
      
      // 处理字段错误
      if (typeof errorData === 'object') {
        const firstErrorField = Object.keys(errorData)[0]
        if (firstErrorField && Array.isArray(errorData[firstErrorField])) {
          ElMessage.error(errorData[firstErrorField][0])
        } else {
          ElMessage.error('更新个人资料失败，请检查输入信息')
        }
      } else {
        ElMessage.error('更新个人资料失败，请稍后重试')
      }
    } else {
      ElMessage.error('更新个人资料失败，请稍后重试')
    }
  } finally {
    // 重置更新状态
    updating.value = false
  }
}

// 修改密码
async function changePassword() {
  if (!passwordFormRef.value) return
  
  try {
    // 表单验证
    await passwordFormRef.value.validate()
    
    // 设置修改密码状态
    changingPassword.value = true
    
    // 调用修改密码接口
    await axios.post('/api/authority/users/change-password/', {
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    
    // 修改成功提示
    ElMessage.success('密码修改成功')
    
    // 重置表单
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    
    // 重置表单验证
    passwordFormRef.value.resetFields()
  } catch (error) {
    console.error('修改密码失败:', error)
    
    // 显示错误信息
    if (error.response && error.response.data) {
      const errorData = error.response.data
      
      // 处理字段错误
      if (typeof errorData === 'object') {
        const firstErrorField = Object.keys(errorData)[0]
        if (firstErrorField && Array.isArray(errorData[firstErrorField])) {
          ElMessage.error(errorData[firstErrorField][0])
        } else if (errorData.detail) {
          ElMessage.error(errorData.detail)
        } else {
          ElMessage.error('修改密码失败，请检查输入信息')
        }
      } else {
        ElMessage.error('修改密码失败，请稍后重试')
      }
    } else {
      ElMessage.error('修改密码失败，请稍后重试')
    }
  } finally {
    // 重置修改密码状态
    changingPassword.value = false
  }
}

// 头像上传前的验证
function beforeAvatarUpload(file) {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

// 头像上传成功的回调
async function handleAvatarSuccess(response) {
  if (response.avatar) {
    // 更新用户头像
    userInfo.value.avatar = response.avatar
    
    // 更新用户状态中的头像
    await userStore.fetchUserProfile()
    
    ElMessage.success('头像更新成功')
  } else {
    ElMessage.error('头像更新失败')
  }
}

// 组件挂载时获取用户信息
onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped lang="scss">
.profile-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.profile-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h2 {
    margin: 0;
    font-size: 20px;
  }
}

.loading-container {
  padding: 20px 0;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
  
  .el-avatar {
    margin-bottom: 15px;
  }
}

.profile-form,
.password-form {
  max-width: 500px;
}
</style>