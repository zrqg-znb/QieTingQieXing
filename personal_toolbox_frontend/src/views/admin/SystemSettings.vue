<template>
  <div class="system-settings">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统设置</span>
          <el-button type="primary" @click="handleAddConfig">
            <el-icon><Plus /></el-icon>添加配置
          </el-button>
        </div>
      </template>

      <el-table :data="configs" style="width: 100%">
        <el-table-column prop="key" label="配置键" />
        <el-table-column prop="value" label="配置值" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="type" label="类型">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" @click="handleEditConfig(row)">
                编辑
              </el-button>
              <el-button type="danger" @click="handleDeleteConfig(row)">
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 配置表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加配置' : '编辑配置'"
      width="500px"
    >
      <el-form
        ref="configFormRef"
        :model="configForm"
        :rules="configFormRules"
        label-width="80px"
      >
        <el-form-item label="配置键" prop="key">
          <el-input 
            v-model="configForm.key"
            :disabled="dialogType === 'edit'"
          />
        </el-form-item>
        <el-form-item label="配置值" prop="value">
          <el-input
            v-if="configForm.type === 'string'"
            v-model="configForm.value"
          />
          <el-input-number
            v-else-if="configForm.type === 'number'"
            v-model="configForm.value"
            :precision="configForm.precision || 0"
          />
          <el-switch
            v-else-if="configForm.type === 'boolean'"
            v-model="configForm.value"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="configForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select
            v-model="configForm.type"
            placeholder="请选择类型"
            :disabled="dialogType === 'edit'"
          >
            <el-option label="字符串" value="string" />
            <el-option label="数字" value="number" />
            <el-option label="布尔值" value="boolean" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitConfig">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 配置列表数据
const configs = ref([])

// 表单相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const configFormRef = ref(null)
const configForm = ref({
  key: '',
  value: '',
  description: '',
  type: 'string'
})

// 表单验证规则
const configFormRules = {
  key: [
    { required: true, message: '请输入配置键', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '配置键只能包含字母、数字和下划线，且必须以字母开头', trigger: 'blur' }
  ],
  value: [
    { required: true, message: '请输入配置值', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ]
}

// 获取配置列表
const fetchConfigs = async () => {
  try {
    const response = await fetch('/api/system/configs')
    const data = await response.json()
    configs.value = data
  } catch (error) {
    ElMessage.error('获取配置列表失败')
  }
}

// 添加配置
const handleAddConfig = () => {
  dialogType.value = 'add'
  configForm.value = {
    key: '',
    value: '',
    description: '',
    type: 'string'
  }
  dialogVisible.value = true
}

// 编辑配置
const handleEditConfig = (config) => {
  dialogType.value = 'edit'
  configForm.value = { ...config }
  dialogVisible.value = true
}

// 删除配置
const handleDeleteConfig = async (config) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该配置吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await fetch(`/api/system/configs/${config.key}`, {
      method: 'DELETE'
    })
    
    ElMessage.success('删除成功')
    await fetchConfigs()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交配置表单
const handleSubmitConfig = async () => {
  if (!configFormRef.value) return
  
  await configFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const url = dialogType.value === 'add' 
          ? '/api/system/configs'
          : `/api/system/configs/${configForm.value.key}`
        const method = dialogType.value === 'add' ? 'POST' : 'PUT'
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(configForm.value)
        })
        
        if (!response.ok) throw new Error('操作失败')
        
        ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
        dialogVisible.value = false
        await fetchConfigs()
      } catch (error) {
        ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

// 初始化
onMounted(() => {
  fetchConfigs()
})
</script>

<style scoped>
.system-settings {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>