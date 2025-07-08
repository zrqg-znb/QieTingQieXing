<template>
  <div class="data-source-editor">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑数据源' : '新建数据源' }}</h2>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="source-form"
    >
      <el-form-item label="数据源名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入数据源名称" />
      </el-form-item>

      <el-form-item label="数据源类型" prop="type">
        <el-select
          v-model="form.type"
          placeholder="请选择数据源类型"
          @change="handleTypeChange"
        >
          <el-option label="MySQL" value="mysql" />
          <el-option label="PostgreSQL" value="postgresql" />
          <el-option label="MongoDB" value="mongodb" />
          <el-option label="Redis" value="redis" />
          <el-option label="REST API" value="api" />
        </el-select>
      </el-form-item>

      <template v-if="form.type === 'api'">
        <el-form-item label="API URL" prop="url">
          <el-input v-model="form.url" placeholder="请输入API地址" />
        </el-form-item>

        <el-form-item label="认证方式" prop="auth_type">
          <el-select v-model="form.auth_type" placeholder="请选择认证方式">
            <el-option label="无认证" value="none" />
            <el-option label="Basic Auth" value="basic" />
            <el-option label="Bearer Token" value="bearer" />
            <el-option label="API Key" value="apikey" />
          </el-select>
        </el-form-item>

        <template v-if="form.auth_type === 'basic'">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>
        </template>

        <el-form-item v-if="form.auth_type === 'bearer'" label="Token" prop="token">
          <el-input v-model="form.token" placeholder="请输入Token" />
        </el-form-item>

        <template v-if="form.auth_type === 'apikey'">
          <el-form-item label="Key名称" prop="api_key_name">
            <el-input v-model="form.api_key_name" placeholder="请输入Key名称" />
          </el-form-item>
          <el-form-item label="Key值" prop="api_key_value">
            <el-input v-model="form.api_key_value" placeholder="请输入Key值" />
          </el-form-item>
          <el-form-item label="传递方式" prop="api_key_in">
            <el-select v-model="form.api_key_in" placeholder="请选择传递方式">
              <el-option label="Header" value="header" />
              <el-option label="Query" value="query" />
            </el-select>
          </el-form-item>
        </template>
      </template>

      <template v-else>
        <el-form-item label="主机地址" prop="host">
          <el-input v-model="form.host" placeholder="请输入主机地址" />
        </el-form-item>

        <el-form-item label="端口" prop="port">
          <el-input-number
            v-model="form.port"
            :min="1"
            :max="65535"
            placeholder="请输入端口号"
          />
        </el-form-item>

        <el-form-item label="数据库名" prop="database">
          <el-input v-model="form.database" placeholder="请输入数据库名" />
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="SSL连接" prop="ssl">
          <el-switch v-model="form.ssl" />
        </el-form-item>

        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="高级选项" name="advanced">
            <el-form-item label="连接池大小" prop="pool_size">
              <el-input-number
                v-model="form.pool_size"
                :min="1"
                :max="100"
                placeholder="请输入连接池大小"
              />
            </el-form-item>

            <el-form-item label="超时时间(秒)" prop="timeout">
              <el-input-number
                v-model="form.timeout"
                :min="1"
                :max="300"
                placeholder="请输入超时时间"
              />
            </el-form-item>

            <el-form-item label="字符集" prop="charset">
              <el-select v-model="form.charset" placeholder="请选择字符集">
                <el-option label="UTF-8" value="utf8" />
                <el-option label="UTF-8mb4" value="utf8mb4" />
                <el-option label="Latin1" value="latin1" />
              </el-select>
            </el-form-item>
          </el-collapse-item>
        </el-collapse>
      </template>

      <el-form-item>
        <el-button type="primary" @click="handleTest">
          <el-icon><Connection /></el-icon>测试连接
        </el-button>
        <el-button type="primary" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '创建数据源' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Connection } from '@element-plus/icons-vue'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const activeCollapse = ref(['advanced'])

const isEdit = computed(() => route.params.id !== undefined)

const form = ref({
  name: '',
  type: '',
  host: '',
  port: null,
  database: '',
  username: '',
  password: '',
  ssl: false,
  pool_size: 10,
  timeout: 30,
  charset: 'utf8mb4',
  url: '',
  auth_type: 'none',
  token: '',
  api_key_name: '',
  api_key_value: '',
  api_key_in: 'header'
})

const rules = {
  name: [{ required: true, message: '请输入数据源名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择数据源类型', trigger: 'change' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口号', trigger: 'blur' }],
  database: [{ required: true, message: '请输入数据库名', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  url: [{ required: true, message: '请输入API地址', trigger: 'blur' }],
  auth_type: [{ required: true, message: '请选择认证方式', trigger: 'change' }],
  token: [{ required: true, message: '请输入Token', trigger: 'blur' }],
  api_key_name: [{ required: true, message: '请输入Key名称', trigger: 'blur' }],
  api_key_value: [{ required: true, message: '请输入Key值', trigger: 'blur' }],
  api_key_in: [{ required: true, message: '请选择传递方式', trigger: 'change' }]
}

const handleTypeChange = () => {
  // 重置表单数据
  Object.keys(form.value).forEach(key => {
    if (key !== 'type' && key !== 'name') {
      form.value[key] = ''
    }
  })

  // 设置默认值
  if (form.value.type === 'mysql') {
    form.value.port = 3306
  } else if (form.value.type === 'postgresql') {
    form.value.port = 5432
  } else if (form.value.type === 'mongodb') {
    form.value.port = 27017
  } else if (form.value.type === 'redis') {
    form.value.port = 6379
  }
}

const fetchDataSource = async () => {
  if (!isEdit.value) return

  try {
    const response = await api.dataViz.getDataSource(route.params.id)
    const sourceData = response.data
    form.value = {
      name: sourceData.name,
      type: sourceData.type,
      host: sourceData.host,
      port: sourceData.port,
      database: sourceData.database,
      username: sourceData.username,
      ssl: sourceData.ssl,
      pool_size: sourceData.pool_size,
      timeout: sourceData.timeout,
      charset: sourceData.charset,
      url: sourceData.url,
      auth_type: sourceData.auth_type,
      api_key_name: sourceData.api_key_name,
      api_key_in: sourceData.api_key_in
    }
  } catch (error) {
    ElMessage.error('获取数据源信息失败')
  }
}

const handleTest = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    const testData = {
      type: form.value.type,
      connection_info: {}
    }

    if (form.value.type === 'api') {
      testData.connection_info = {
        url: form.value.url,
        auth_type: form.value.auth_type,
        auth_config: {}
      }

      switch (form.value.auth_type) {
        case 'basic':
          testData.connection_info.auth_config = {
            username: form.value.username,
            password: form.value.password
          }
          break
        case 'bearer':
          testData.connection_info.auth_config = {
            token: form.value.token
          }
          break
        case 'apikey':
          testData.connection_info.auth_config = {
            key_name: form.value.api_key_name,
            key_value: form.value.api_key_value,
            key_in: form.value.api_key_in
          }
          break
      }
    } else {
      testData.connection_info = {
        host: form.value.host,
        port: form.value.port,
        database: form.value.database,
        username: form.value.username,
        password: form.value.password,
        ssl: form.value.ssl,
        pool_size: form.value.pool_size,
        timeout: form.value.timeout,
        charset: form.value.charset
      }
    }

    await api.dataviz.testDataSourceConnection(testData)
    ElMessage.success('连接测试成功')
  } catch (error) {
    ElMessage.error('连接测试失败：' + error.message)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    const sourceData = {
      name: form.value.name,
      type: form.value.type
    }

    if (form.value.type === 'api') {
      sourceData.url = form.value.url
      sourceData.auth_type = form.value.auth_type
      sourceData.auth_config = {}

      switch (form.value.auth_type) {
        case 'basic':
          sourceData.auth_config = {
            username: form.value.username,
            password: form.value.password
          }
          break
        case 'bearer':
          sourceData.auth_config = {
            token: form.value.token
          }
          break
        case 'apikey':
          sourceData.auth_config = {
            key_name: form.value.api_key_name,
            key_value: form.value.api_key_value,
            key_in: form.value.api_key_in
          }
          break
      }
    } else {
      sourceData.connection_info = {
        host: form.value.host,
        port: form.value.port,
        database: form.value.database,
        username: form.value.username,
        password: form.value.password,
        ssl: form.value.ssl,
        pool_size: form.value.pool_size,
        timeout: form.value.timeout,
        charset: form.value.charset
      }
    }

    if (isEdit.value) {
      await api.dataviz.updateDataSource(route.params.id, sourceData)
      ElMessage.success('数据源更新成功')
    } else {
      await api.dataviz.createDataSource(sourceData)
      ElMessage.success('数据源创建成功')
    }

    router.push('/data-viz/sources')
  } catch (error) {
    if (error.name === 'ValidationError') return
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const handleCancel = () => {
  router.back()
}

onMounted(() => {
  fetchDataSource()
})
</script>

<style scoped>
.data-source-editor {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.source-form {
  max-width: 800px;
}

:deep(.el-collapse-item__content) {
  padding: 20px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}
</style>