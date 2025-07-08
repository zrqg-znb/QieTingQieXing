<template>
  <div class="loading-state">
    <el-skeleton
      v-if="type === 'skeleton'"
      :rows="rows"
      animated
      :loading="true"
    >
      <template #template>
        <slot name="skeleton">
          <el-skeleton-item
            v-for="i in rows"
            :key="i"
            variant="p"
            style="width: 100%"
          />
        </slot>
      </template>
    </el-skeleton>

    <div v-else class="spinner-container">
      <el-icon class="spinner" :size="size">
        <Loading />
      </el-icon>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
  </div>
</template>

<script setup>
import { Loading } from '@element-plus/icons-vue'

defineProps({
  type: {
    type: String,
    default: 'spinner',
    validator: (value) => ['spinner', 'skeleton'].includes(value)
  },
  text: {
    type: String,
    default: '加载中...'
  },
  size: {
    type: Number,
    default: 32
  },
  rows: {
    type: Number,
    default: 3
  }
})
</script>

<style scoped>
.loading-state {
  width: 100%;
  height: 100%;
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner-container {
  text-align: center;
}

.spinner {
  animation: rotate 2s linear infinite;
}

.loading-text {
  margin-top: 12px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>