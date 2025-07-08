<template>
  <div class="dashboard-detail">
    <div class="page-header">
      <h2>{{ dashboard.name }}</h2>
      <div class="header-actions">
        <el-button-group>
          <el-button type="primary" @click="handleEdit">
            <el-icon><Edit /></el-icon>编辑
          </el-button>
          <el-button type="primary" @click="handleShare">
            <el-icon><Share /></el-icon>分享
          </el-button>
          <el-button type="primary" @click="handleExport">
            <el-icon><Download /></el-icon>导出
          </el-button>
        </el-button-group>
      </div>
    </div>

    <el-descriptions :column="3" border>
      <el-descriptions-item label="创建时间">
        {{ formatDate(dashboard.created_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="更新时间">
        {{ formatDate(dashboard.updated_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="创建者">
        {{ dashboard.creator_name }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="dashboard-description" v-if="dashboard.description">
      <p>{{ dashboard.description }}</p>
    </div>

    <div class="dashboard-grid" ref="gridContainer">
      <!-- 使用Grid布局展示图表 -->
      <template v-for="chart in dashboard.charts" :key="chart.id">
        <div class="chart-container" :style="getChartStyle(chart)">
          <div class="chart-header">
            <h3>{{ chart.name }}</h3>
            <el-dropdown trigger="click" @command="handleChartCommand($event, chart.id)">
              <el-button type="text">
                <el-icon><More /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="refresh">刷新</el-dropdown-item>
                  <el-dropdown-item command="fullscreen">全屏</el-dropdown-item>
                  <el-dropdown-item command="remove" divided type="danger">移除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div class="chart-content" :id="`chart-${chart.id}`"></div>
        </div>
      </template>
    </div>

    <!-- 分享对话框 -->
    <el-dialog v-model="shareDialogVisible" title="分享仪表盘" width="500px">
      <el-form :model="shareForm" label-width="100px">
        <el-form-item label="访问链接">
          <el-input v-model="shareForm.url" readonly>
            <template #append>
              <el-button @click="copyShareLink">复制</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="过期时间">
          <el-date-picker
            v-model="shareForm.expireTime"
            type="datetime"
            placeholder="选择过期时间"
            :min-time="new Date()"
          />
        </el-form-item>
        <el-form-item label="访问密码">
          <el-input v-model="shareForm.password" placeholder="可选，留空表示无密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="shareDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleShareSubmit">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Share, Download, More } from '@element-plus/icons-vue'
import api from '@/api'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const dashboard = ref({
  name: '',
  description: '',
  created_at: '',
  updated_at: '',
  creator_name: '',
  charts: []
})

const shareDialogVisible = ref(false)
const shareForm = ref({
  url: '',
  expireTime: '',
  password: ''
})

const chartInstances = ref(new Map())

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const getChartStyle = (chart) => {
  return {
    gridColumn: `span ${chart.width || 1}`,
    gridRow: `span ${chart.height || 1}`,
    minHeight: `${(chart.height || 1) * 200}px`
  }
}

const fetchDashboard = async () => {
  try {
    const response = await api.dataViz.getDashboard(route.params.id)
    dashboard.value = response.data
    initCharts()
  } catch (error) {
    ElMessage.error('获取仪表盘数据失败')
  }
}

const initCharts = () => {
  // 清除旧的图表实例
  chartInstances.value.forEach(instance => instance.dispose())
  chartInstances.value.clear()

  // 初始化新的图表
  dashboard.value.charts.forEach(chart => {
    const chartDom = document.getElementById(`chart-${chart.id}`)
    if (chartDom) {
      const instance = echarts.init(chartDom)
      instance.setOption(chart.options)
      chartInstances.value.set(chart.id, instance)
    }
  })
}

const handleEdit = () => {
  router.push(`/data-viz/dashboard/${route.params.id}/edit`)
}

const handleShare = () => {
  shareForm.value = {
    url: `${window.location.origin}/share/dashboard/${route.params.id}`,
    expireTime: '',
    password: ''
  }
  shareDialogVisible.value = true
}

const handleShareSubmit = async () => {
  try {
    await api.dataViz.shareDashboard(route.params.id, {
      expire_time: shareForm.value.expireTime,
      password: shareForm.value.password
    })
    ElMessage.success('分享设置已保存')
    shareDialogVisible.value = false
  } catch (error) {
    ElMessage.error('保存分享设置失败')
  }
}

const copyShareLink = () => {
  navigator.clipboard.writeText(shareForm.value.url)
    .then(() => ElMessage.success('链接已复制'))
    .catch(() => ElMessage.error('复制失败'))
}

const handleExport = async () => {
  try {
    const response = await api.dataViz.exportDashboard(route.params.id)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = `${dashboard.value.name}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleChartCommand = async (command, chartId) => {
  switch (command) {
    case 'edit':
      router.push(`/data-viz/charts/${chartId}/edit`)
      break
    case 'refresh':
      await refreshChart(chartId)
      break
    case 'fullscreen':
      toggleFullscreen(chartId)
      break
    case 'remove':
      await removeChart(chartId)
      break
  }
}

const refreshChart = async (chartId) => {
  try {
    const response = await api.dataViz.getChartData(chartId)
    const chart = dashboard.value.charts.find(c => c.id === chartId)
    if (chart) {
      chart.options.series = response.data
      const instance = chartInstances.value.get(chartId)
      if (instance) {
        instance.setOption(chart.options)
      }
    }
  } catch (error) {
    ElMessage.error('刷新图表数据失败')
  }
}

const toggleFullscreen = (chartId) => {
  const chartDom = document.getElementById(`chart-${chartId}`)
  if (chartDom) {
    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      chartDom.requestFullscreen()
    }
  }
}

const removeChart = async (chartId) => {
  try {
    await ElMessageBox.confirm('确定要从仪表盘中移除这个图表吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.dataViz.removeChartFromDashboard(route.params.id, chartId)
    ElMessage.success('图表已移除')
    await fetchDashboard()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除图表失败')
    }
  }
}

const handleResize = () => {
  chartInstances.value.forEach(instance => {
    instance.resize()
  })
}

onMounted(() => {
  fetchDashboard()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  // 清除所有图表实例
  chartInstances.value.forEach(instance => instance.dispose())
})
</script>

<style scoped>
.dashboard-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-description {
  margin: 20px 0;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.chart-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #dcdfe6;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
}

.chart-content {
  height: 100%;
  min-height: 300px;
}
</style>