<template>
  <div class="search-bar">
    <el-form :inline="true" :model="formData" @submit.prevent="handleSearch">
      <slot name="prefix"></slot>

      <el-form-item v-if="showKeyword">
        <el-input
          v-model="formData.keyword"
          :placeholder="keywordPlaceholder"
          clearable
          @clear="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <slot></slot>

      <el-form-item>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button v-if="showReset" @click="handleReset">
          <el-icon><Refresh /></el-icon>重置
        </el-button>
      </el-form-item>

      <slot name="suffix"></slot>
    </el-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'

const props = defineProps({
  showKeyword: {
    type: Boolean,
    default: true
  },
  keywordPlaceholder: {
    type: String,
    default: '请输入关键词搜索'
  },
  showReset: {
    type: Boolean,
    default: true
  },
  initialValues: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['search', 'reset'])

const formData = ref({
  keyword: '',
  ...props.initialValues
})

watch(
  () => props.initialValues,
  (newValues) => {
    formData.value = {
      keyword: '',
      ...newValues
    }
  },
  { deep: true }
)

const handleSearch = () => {
  emit('search', { ...formData.value })
}

const handleReset = () => {
  formData.value = {
    keyword: '',
    ...props.initialValues
  }
  emit('reset')
  emit('search', { ...formData.value })
}
</script>

<style scoped>
.search-bar {
  margin-bottom: 24px;
  padding: 24px;
  background-color: var(--el-bg-color);
  border-radius: var(--el-border-radius-base);
}

.el-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin: 0;
}

.el-form-item {
  margin: 0;
}

:deep(.el-form-item__content) {
  margin: 0 !important;
}
</style>