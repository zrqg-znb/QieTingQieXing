<template>
  <div class="data-source-list">
    <div class="page-header">
      <h2>数据源管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建数据源
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="dataSources"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="数据源名称" min-width="200">
        <template #default="{ row }">
          <div class="source-name">
            <el-icon><DataAnalysis /></el-icon>
            <span>{{ row.name }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="type" label="数据源类型" width="120">
        <template #default="{ row }">
          <el-tag>{{ row.type }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="connection_info" label="连接信息" min-width="300">
        <template #default="{ row }">
          <el-tooltip
            :content="getConnectionInfo(row)"
            placement="top"
            :hide-after="0"
          >
            <span class="connection-info">{{ getConnectionInfo(row) }}</span>
          </el-tooltip>
        </template>
      </el-table-column>

      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'connected' ? 'success' : 'danger'">
            {{ row.status === 'connected' ? '已连接' : '未连接' }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>

      <el-table-column label="操作" width="320" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button 
              type="primary" 
              :loading="row.testing"
              @click="handleTest(row)"
            >
              <el-icon><Connection /></el-icon>测试连接
            </el-button>
            <el-button type="primary" @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>编辑
            </el-button>
            <el-button type="danger" @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next"
      class="pagination"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, DataAnalysis, Connection, Edit, Delete } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const loading = ref(false)
const dataSources = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const getConnectionInfo = (dataSource) => {
  switch (dataSource.type) {
    case 'mysql':
    case 'postgresql':
      return `${dataSource.host}:${dataSource.port}/${dataSource.database}`
    case 'mongodb':
      return `mongodb://${dataSource.host}:${dataSource.port}/${dataSource.database}`
    case 'redis':
      return `redis://${dataSource.host}:${dataSource.port}/${dataSource.database}`
    case 'api':
      return dataSource.url
    default:
      return '未知连接信息'
  }
}

const fetchDataSources = async () => {
  loading.value = true
  try {
    const response = await api.dataViz.getDataSources({
      page: currentPage.value,
      page_size: pageSize.value
    })
    dataSources.value = response.data.results
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push('/data-viz/sources/new')
}

const handleTest = async (dataSource) => {
  dataSource.testing = true
  try {
    await api.dataViz.testDataSource(dataSource.id)
    ElMessage.success('连接测试成功')
    await fetchDataSources() // 刷新状态
  } catch (error) {
    ElMessage.error('连接测试失败：' + error.message)
  } finally {
    dataSource.testing = false
  }
}

const handleEdit = (dataSource) => {
  router.push(`/data-viz/sources/${dataSource.id}/edit`)
}

const handleDelete = async (dataSource) => {
  try {
    await ElMessageBox.confirm('确定要删除这个数据源吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
      message: h('p', null, [
        h('span', null, '删除数据源将同时删除所有使用该数据源的图表，是否继续？')
      ])
    })
    
    await api.dataViz.deleteDataSource(dataSource.id)
    ElMessage.success('删除成功')
    await fetchDataSources()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchDataSources()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchDataSources()
}

onMounted(() => {
  fetchDataSources()
})
</script>

<style scoped>
.data-source-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.source-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.connection-info {
  display: inline-block;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>