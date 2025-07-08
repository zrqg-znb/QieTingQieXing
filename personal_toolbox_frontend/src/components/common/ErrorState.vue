<template>
  <div class="error-state">
    <el-result
      icon="error"
      :title="title"
      :sub-title="description"
    >
      <template #extra>
        <slot name="actions">
          <el-button type="primary" @click="$emit('retry')">
            重试
          </el-button>
          <el-button @click="$emit('back')">
            返回
          </el-button>
        </slot>
      </template>
    </el-result>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '操作失败'
  },
  description: {
    type: String,
    default: '请稍后重试或联系管理员'
  }
})

defineEmits(['retry', 'back'])
</script>

<style scoped>
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px;
}
</style>