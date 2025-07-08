<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="dialog-content">
      <el-icon v-if="showIcon" :class="['dialog-icon', type]">
        <Warning v-if="type === 'warning'" />
        <InfoFilled v-else-if="type === 'info'" />
        <CircleCheck v-else-if="type === 'success'" />
        <CircleClose v-else-if="type === 'error'" />
      </el-icon>
      
      <div class="message-content">
        <p class="message">{{ message }}</p>
        <p v-if="description" class="description">{{ description }}</p>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">{{ cancelText }}</el-button>
        <el-button
          :type="confirmButtonType"
          :loading="loading"
          @click="handleConfirm"
        >
          {{ confirmText }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Warning, InfoFilled, CircleCheck, CircleClose } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '确认'
  },
  message: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['warning', 'info', 'success', 'error'].includes(value)
  },
  width: {
    type: String,
    default: '420px'
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  confirmText: {
    type: String,
    default: '确认'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const confirmButtonType = computed(() => {
  const typeMap = {
    warning: 'warning',
    info: 'primary',
    success: 'success',
    error: 'danger'
  }
  return typeMap[props.type] || 'primary'
})

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}

const handleClose = () => {
  emit('cancel')
}
</script>

<style scoped>
.dialog-content {
  display: flex;
  align-items: flex-start;
  padding: 10px 0;
}

.dialog-icon {
  font-size: 24px;
  margin-right: 16px;
}

.dialog-icon.warning {
  color: var(--el-color-warning);
}

.dialog-icon.info {
  color: var(--el-color-info);
}

.dialog-icon.success {
  color: var(--el-color-success);
}

.dialog-icon.error {
  color: var(--el-color-danger);
}

.message-content {
  flex: 1;
}

.message {
  margin: 0;
  font-size: 16px;
  line-height: 24px;
  color: var(--el-text-color-primary);
}

.description {
  margin: 8px 0 0;
  font-size: 14px;
  line-height: 20px;
  color: var(--el-text-color-secondary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>