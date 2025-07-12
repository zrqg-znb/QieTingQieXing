<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>注册</h2>
        <p>创建您的切听切行个人空间账号</p>
      </div>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="registerForm.username" 
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item label="昵称" prop="nickname">
          <el-input 
            v-model="registerForm.nickname" 
            placeholder="请输入昵称"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="registerForm.email" 
            type="email"
            placeholder="请输入邮箱"
            prefix-icon="el-icon-message"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="loading" 
            class="register-button"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-footer">
        <p>已有账号? <el-link type="primary" @click="navigateToLogin">立即登录</el-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const registerFormRef = ref(null)

// 表单数据
const registerForm = reactive({
  username: '',
  nickname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 加载状态
const loading = ref(false)

// 验证密码是否一致
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度应为2-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ]
}

// 导航到登录页面
function navigateToLogin() {
  router.push('/login')
}

// 处理注册
async function handleRegister() {
  if (!registerFormRef.value) return
  
  try {
    // 表单验证
    await registerFormRef.value.validate()
    
    // 设置加载状态
    loading.value = true
    
    // 调用注册接口
    await userStore.register({
      username: registerForm.username,
      nickname: registerForm.nickname,
      email: registerForm.email,
      password: registerForm.password
    })
    
    // 注册成功提示
    ElMessage.success('注册成功，请登录')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    
    // 显示错误信息
    if (error.response && error.response.data) {
      const errorData = error.response.data
      
      // 处理字段错误
      if (typeof errorData === 'object') {
        const firstErrorField = Object.keys(errorData)[0]
        if (firstErrorField && Array.isArray(errorData[firstErrorField])) {
          ElMessage.error(errorData[firstErrorField][0])
        } else {
          ElMessage.error('注册失败，请检查输入信息')
        }
      } else {
        ElMessage.error('注册失败，请稍后重试')
      }
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    // 重置加载状态
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
  
  h2 {
    font-size: 24px;
    margin-bottom: 8px;
    color: #303133;
  }
  
  p {
    color: #909399;
    font-size: 14px;
  }
}

.register-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.register-footer {
  margin-top: 20px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}
</style>