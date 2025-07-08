<template>
  <el-tag
    :type="tagType"
    :effect="effect"
    :size="size"
    :class="['status-tag', status]"
  >
    <el-icon v-if="showIcon" class="status-icon">
      <component :is="iconComponent" />
    </el-icon>
    <slot>{{ label }}</slot>
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'
import {
  CircleCheck,
  CircleClose,
  Warning,
  Loading,
  InfoFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) =>
      ['success', 'error', 'warning', 'info', 'processing'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  effect: {
    type: String,
    default: 'light',
    validator: (value) => ['dark', 'light', 'plain'].includes(value)
  },
  size: {
    type: String,
    default: 'default',
    validator: (value) => ['large', 'default', 'small'].includes(value)
  }
})

const tagType = computed(() => {
  const typeMap = {
    success: 'success',
    error: 'danger',
    warning: 'warning',
    info: 'info',
    processing: 'info'
  }
  return typeMap[props.status]
})

const iconComponent = computed(() => {
  const iconMap = {
    success: CircleCheck,
    error: CircleClose,
    warning: Warning,
    info: InfoFilled,
    processing: Loading
  }
  return iconMap[props.status]
})
</script>

<style scoped>
.status-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.status-icon {
  margin-right: 2px;
}

.status-tag.processing .status-icon {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>