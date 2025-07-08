<template>
  <div class="chart-list">
    <div class="page-header">
      <h2>图表管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建图表
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="charts"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="图表名称" min-width="200">
        <template #default="{ row }">
          <div class="chart-name">
            <el-icon><PieChart /></el-icon>
            <span>{{ row.name }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="type" label="图表类型" width="120">
        <template #default="{ row }">
          <el-tag>{{ row.type }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="data_source" label="数据源" min-width="180" />

      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>

      <el-table-column prop="creator" label="创建者" width="120" />

      <el-table-column label="操作" width="250" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handlePreview(row)">
              <el-icon><View /></el-icon>预览
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

    <!-- 图表预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="currentChart?.name"
      width="80%"
      destroy-on-close
    >
      <div class="chart-preview" ref="chartPreview"></div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, PieChart, View, Edit, Delete } from '@element-plus/icons-vue'
import api from '@/api'
import * as echarts from 'echarts'

const router = useRouter()
const loading = ref(false)
const charts = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const previewDialogVisible = ref(false)
const currentChart = ref(null)
const chartPreview = ref(null)
let chartInstance = null

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const fetchCharts = async () => {
  loading.value = true
  try {
    const response = await api.dataViz.getCharts({
      page: currentPage.value,
      page_size: pageSize.value
    })
    charts.value = response.data.results
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取图表列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push('/data-viz/charts/new')
}

const handlePreview = async (chart) => {
  currentChart.value = chart
  previewDialogVisible.value = true

  // 等待DOM更新后初始化图表
  await nextTick()
  if (chartInstance) {
    chartInstance.dispose()
  }

  try {
    const response = await api.dataViz.getChartData(chart.id)
    const options = {
      ...chart.options,
      series: response.data
    }

    chartInstance = echarts.init(chartPreview.value)
    chartInstance.setOption(options)

    // 监听窗口大小变化
    const handleResize = () => chartInstance?.resize()
    window.addEventListener('resize', handleResize)

    // 清理函数
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize)
      chartInstance?.dispose()
      chartInstance = null
    })
  } catch (error) {
    ElMessage.error('加载图表数据失败')
  }
}

const handleEdit = (chart) => {
  router.push(`/data-viz/charts/${chart.id}/edit`)
}

const handleDelete = async (chart) => {
  try {
    await ElMessageBox.confirm('确定要删除这个图表吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.dataViz.deleteChart(chart.id)
    ElMessage.success('删除成功')
    await fetchCharts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchCharts()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchCharts()
}

onMounted(() => {
  fetchCharts()
})
</script>

<style scoped>
.chart-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.chart-preview {
  height: 500px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style>