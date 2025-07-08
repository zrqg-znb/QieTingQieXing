<template>
  <div class="chart-detail">
    <div class="page-header">
      <h2>{{ chart.name }}</h2>
      <div class="header-actions">
        <el-button-group>
          <el-button type="primary" @click="handleRefresh">
            <el-icon><Refresh /></el-icon>刷新数据
          </el-button>
          <el-button type="primary" @click="handleEdit">
            <el-icon><Edit /></el-icon>编辑
          </el-button>
          <el-button type="primary" @click="handleExport">
            <el-icon><Download /></el-icon>导出
          </el-button>
        </el-button-group>
      </div>
    </div>

    <el-descriptions :column="3" border>
      <el-descriptions-item label="图表类型">
        <el-tag>{{ chart.type }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="数据源">
        {{ chart.data_source_name }}
      </el-descriptions-item>
      <el-descriptions-item label="创建者">
        {{ chart.creator_name }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ formatDate(chart.created_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="更新时间">
        {{ formatDate(chart.updated_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="最后刷新">
        {{ formatDate(chart.last_refresh_at) }}
      </el-descriptions-item>
    </el-descriptions>

    <el-card class="query-info">
      <template #header>
        <div class="card-header">
          <span>数据查询</span>
          <el-tooltip content="查看执行计划" placement="top">
            <el-button type="primary" link @click="handleShowPlan">
              <el-icon><Monitor /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </template>
      <pre><code>{{ chart.query }}</code></pre>
    </el-card>

    <div class="chart-container" ref="chartContainer">
      <!-- 图表将在这里渲染 -->
    </div>

    <!-- 执行计划对话框 -->
    <el-dialog
      v-model="planDialogVisible"
      title="查询执行计划"
      width="80%"
      destroy-on-close
    >
      <pre><code>{{ queryPlan }}</code></pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Refresh, Edit, Download, Monitor } from '@element-plus/icons-vue'
import api from '@/api'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const chartContainer = ref(null)
let chartInstance = null

const chart = ref({
  name: '',
  type: '',
  data_source_name: '',
  creator_name: '',
  created_at: '',
  updated_at: '',
  last_refresh_at: '',
  query: '',
  options: {}
})

const planDialogVisible = ref(false)
const queryPlan = ref('')

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const fetchChartData = async () => {
  try {
    const response = await api.dataViz.getChart(route.params.id)
    chart.value = response.data
    initChart()
  } catch (error) {
    ElMessage.error('获取图表数据失败')
  }
}

const initChart = async () => {
  try {
    const response = await api.dataViz.getChartData(route.params.id)
    
    if (!chartInstance) {
      chartInstance = echarts.init(chartContainer.value)
    }

    const options = {
      ...chart.value.options,
      series: response.data
    }

    chartInstance.setOption(options)
  } catch (error) {
    ElMessage.error('加载图表数据失败')
  }
}

const handleRefresh = async () => {
  try {
    await api.dataViz.refreshChartData(route.params.id)
    await initChart()
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新数据失败')
  }
}

const handleEdit = () => {
  router.push(`/data-viz/chart/${route.params.id}/edit`)
}

const handleExport = async () => {
  try {
    const response = await api.dataViz.exportChart(route.params.id)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = `${chart.value.name}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleShowPlan = async () => {
  try {
    const response = await api.dataViz.getQueryPlan(route.params.id)
    queryPlan.value = response.data
    planDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取执行计划失败')
  }
}

// 监听窗口大小变化，重绘图表
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  fetchChartData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.chart-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.query-info {
  margin: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.query-info pre {
  margin: 0;
  padding: 10px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  overflow-x: auto;
}

.chart-container {
  margin-top: 20px;
  height: 600px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  padding: 20px;
}

:deep(.el-dialog__body) pre {
  margin: 0;
  padding: 15px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>