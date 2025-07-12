<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>登录</h2>
        <p>欢迎回到切听切行个人空间系统</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <div class="form-actions">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" :underline="false">忘记密码?</el-link>
        </div>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="loading" 
            class="login-button"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>还没有账号? <el-link type="primary" @click="navigateToRegister">立即注册</el-link></p>
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
const loginFormRef = ref(null)

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 记住我选项
const rememberMe = ref(false)

// 加载状态
const loading = ref(false)

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ]
}

// 导航到注册页面
function navigateToRegister() {
  router.push('/register')
}

// 处理登录
async function handleLogin() {
  if (!loginFormRef.value) return
  
  try {
    // 表单验证
    await loginFormRef.value.validate()
    
    // 设置加载状态
    loading.value = true
    
    // 调用登录接口
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password,
      remember: rememberMe.value
    })
    
    // 登录成功提示
    ElMessage.success('登录成功')
    
    // 跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    
    // 显示错误信息
    if (error.response && error.response.data) {
      const { non_field_errors, detail } = error.response.data
      if (non_field_errors) {
        ElMessage.error(non_field_errors[0])
      } else if (detail) {
        ElMessage.error(detail)
      } else {
        ElMessage.error('登录失败，请检查用户名和密码')
      }
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  } finally {
    // 重置加载状态
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.login-header {
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

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}
</style>