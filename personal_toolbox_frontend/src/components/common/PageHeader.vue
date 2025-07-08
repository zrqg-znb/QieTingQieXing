<template>
  <div class="page-header">
    <div class="header-content">
      <div class="title-section">
        <h2 class="title">{{ title }}</h2>
        <p v-if="description" class="description">{{ description }}</p>
      </div>
      
      <div v-if="$slots.actions" class="actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <el-divider v-if="showDivider" />
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  showDivider: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.title-section {
  flex: 1;
}

.title {
  margin: 0;
  font-size: 24px;
  line-height: 32px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.description {
  margin: 8px 0 0;
  font-size: 14px;
  line-height: 22px;
  color: var(--el-text-color-secondary);
}

.actions {
  margin-left: 48px;
  display: flex;
  gap: 12px;
  align-items: center;
}
</style>