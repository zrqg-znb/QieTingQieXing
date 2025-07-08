<template>
  <div class="empty-state">
    <el-empty
      :image="image"
      :image-size="200"
      :description="description"
    >
      <template #default>
        <slot>
          <el-button v-if="actionText" type="primary" @click="$emit('action')">
            {{ actionText }}
          </el-button>
        </slot>
      </template>
    </el-empty>
  </div>
</template>

<script setup>
defineProps({
  image: {
    type: String,
    default: undefined
  },
  description: {
    type: String,
    default: '暂无数据'
  },
  actionText: {
    type: String,
    default: ''
  }
})

defineEmits(['action'])
</script>

<style scoped>
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  text-align: center;
}
</style>