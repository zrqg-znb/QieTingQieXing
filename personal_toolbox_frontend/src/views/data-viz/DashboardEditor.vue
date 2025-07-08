<template>
  <div class="dashboard-editor">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑仪表盘' : '新建仪表盘' }}</h2>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="dashboard-form"
    >
      <el-form-item label="仪表盘名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入仪表盘名称" />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入仪表盘描述"
        />
      </el-form-item>

      <el-form-item label="布局设置">
        <el-radio-group v-model="form.layout.type">
          <el-radio-button label="grid">网格布局</el-radio-button>
          <el-radio-button label="flex">弹性布局</el-radio-button>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="图表列表">
        <div class="charts-container">
          <div class="charts-list">
            <el-table
              :data="form.charts"
              style="width: 100%"
              :max-height="400"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              
              <el-table-column prop="name" label="图表名称">
                <template #default="{ row }">
                  <div class="chart-name">
                    <el-icon><PieChart /></el-icon>
                    <span>{{ row.name }}</span>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="type" label="类型" width="120">
                <template #default="{ row }">
                  <el-tag>{{ row.type }}</el-tag>
                </template>
              </el-table-column>

              <el-table-column label="尺寸" width="200">
                <template #default="{ row }">
                  <el-input-number
                    v-model="row.width"
                    :min="1"
                    :max="12"
                    size="small"
                    class="size-input"
                  >
                    <template #prefix>宽</template>
                  </el-input-number>
                  <el-input-number
                    v-model="row.height"
                    :min="1"
                    :max="12"
                    size="small"
                    class="size-input"
                  >
                    <template #prefix>高</template>
                  </el-input-number>
                </template>
              </el-table-column>

              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row, $index }">
                  <el-button-group>
                    <el-button
                      type="primary"
                      link
                      @click="handlePreviewChart(row)"
                    >
                      <el-icon><View /></el-icon>
                    </el-button>
                    <el-button
                      type="danger"
                      link
                      @click="handleRemoveChart($index)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>

            <div class="charts-actions">
              <el-button type="primary" @click="handleAddCharts">
                <el-icon><Plus /></el-icon>添加图表
              </el-button>
              <el-button
                type="danger"
                :disabled="!selectedCharts.length"
                @click="handleRemoveSelected"
              >
                <el-icon><Delete /></el-icon>删除选中
              </el-button>
            </div>
          </div>

          <div class="layout-preview">
            <h3>布局预览</h3>
            <div
              :class="['preview-container', `layout-${form.layout.type}`]"
              ref="previewContainer"
            >
              <div
                v-for="chart in form.charts"
                :key="chart.id"
                :class="['chart-item', `span-${chart.width}`]"
                :style="getChartStyle(chart)"
              >
                <div class="chart-header">
                  <span>{{ chart.name }}</span>
                </div>
                <div class="chart-content" :id="`preview-${chart.id}`"></div>
              </div>
            </div>
          </div>
        </div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '创建仪表盘' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>

    <!-- 添加图表对话框 -->
    <el-dialog
      v-model="addChartsDialogVisible"
      title="添加图表"
      width="60%"
    >
      <el-table
        :data="availableCharts"
        style="width: 100%"
        @selection-change="handleAvailableChartsChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="图表名称" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="data_source_name" label="数据源" width="180" />
      </el-table>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addChartsDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :disabled="!selectedAvailableCharts.length"
            @click="handleConfirmAddCharts"
          >
            确认添加
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 图表预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="currentPreviewChart?.name"
      width="80%"
      destroy-on-close
    >
      <div class="chart-preview" ref="chartPreview"></div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, PieChart, View, Delete } from '@element-plus/icons-vue'
import api from '@/api'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const previewContainer = ref(null)
const chartPreview = ref(null)

const isEdit = computed(() => route.params.id !== undefined)

const form = ref({
  name: '',
  description: '',
  layout: {
    type: 'grid'
  },
  charts: []
})

const rules = {
  name: [{ required: true, message: '请输入仪表盘名称', trigger: 'blur' }]
}

const selectedCharts = ref([])
const addChartsDialogVisible = ref(false)
const availableCharts = ref([])
const selectedAvailableCharts = ref([])

const previewDialogVisible = ref(false)
const currentPreviewChart = ref(null)
let previewChartInstance = null

// 图表预览实例Map
const chartInstances = ref(new Map())

const fetchDashboardData = async () => {
  if (!isEdit.value) return

  try {
    const response = await api.dataViz.getDashboard(route.params.id)
    const dashboardData = response.data
    form.value = {
      name: dashboardData.name,
      description: dashboardData.description,
      layout: dashboardData.layout,
      charts: dashboardData.charts.map(chart => ({
        ...chart,
        width: chart.width || 6,
        height: chart.height || 4
      }))
    }
    initChartPreviews()
  } catch (error) {
    ElMessage.error('获取仪表盘数据失败')
  }
}

const fetchAvailableCharts = async () => {
  try {
    const response = await api.dataViz.getAvailableCharts()
    availableCharts.value = response.data
  } catch (error) {
    ElMessage.error('获取可用图表失败')
  }
}

const getChartStyle = (chart) => {
  if (form.value.layout.type === 'grid') {
    return {
      gridColumn: `span ${chart.width || 1}`,
      gridRow: `span ${chart.height || 1}`,
      minHeight: `${(chart.height || 1) * 100}px`
    }
  }
  return {
    width: `${(chart.width || 1) * 8.33}%`,
    height: `${(chart.height || 1) * 100}px`
  }
}

const initChartPreviews = () => {
  // 清除旧的图表实例
  chartInstances.value.forEach(instance => instance.dispose())
  chartInstances.value.clear()

  // 初始化新的图表预览
  form.value.charts.forEach(chart => {
    const chartDom = document.getElementById(`preview-${chart.id}`)
    if (chartDom) {
      const instance = echarts.init(chartDom)
      instance.setOption(chart.options)
      chartInstances.value.set(chart.id, instance)
    }
  })
}

const handleSelectionChange = (selection) => {
  selectedCharts.value = selection
}

const handleAvailableChartsChange = (selection) => {
  selectedAvailableCharts.value = selection
}

const handleAddCharts = () => {
  addChartsDialogVisible.value = true
  fetchAvailableCharts()
}

const handleConfirmAddCharts = () => {
  form.value.charts.push(
    ...selectedAvailableCharts.value.map(chart => ({
      ...chart,
      width: 6,
      height: 4
    }))
  )
  addChartsDialogVisible.value = false
  selectedAvailableCharts.value = []
  initChartPreviews()
}

const handleRemoveChart = (index) => {
  const chart = form.value.charts[index]
  const instance = chartInstances.value.get(chart.id)
  if (instance) {
    instance.dispose()
    chartInstances.value.delete(chart.id)
  }
  form.value.charts.splice(index, 1)
}

const handleRemoveSelected = () => {
  selectedCharts.value.forEach(chart => {
    const index = form.value.charts.findIndex(c => c.id === chart.id)
    if (index > -1) {
      handleRemoveChart(index)
    }
  })
  selectedCharts.value = []
}

const handlePreviewChart = async (chart) => {
  currentPreviewChart.value = chart
  previewDialogVisible.value = true

  await nextTick()
  if (previewChartInstance) {
    previewChartInstance.dispose()
  }
  previewChartInstance = echarts.init(chartPreview.value)
  previewChartInstance.setOption(chart.options)
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    const dashboardData = {
      name: form.value.name,
      description: form.value.description,
      layout: form.value.layout,
      charts: form.value.charts.map(({ id, width, height }) => ({
        id,
        width,
        height
      }))
    }

    if (isEdit.value) {
      await api.dataViz.updateDashboard(route.params.id, dashboardData)
      ElMessage.success('仪表盘更新成功')
    } else {
      await api.dataViz.createDashboard(dashboardData)
      ElMessage.success('仪表盘创建成功')
    }

    router.push('/data-viz/dashboard')
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error(isEdit.value ? '更新仪表盘失败' : '创建仪表盘失败')
    }
  }
}

const handleCancel = () => {
  router.back()
}

const handleResize = () => {
  chartInstances.value.forEach(instance => {
    instance.resize()
  })
}

onMounted(() => {
  fetchDashboardData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  // 清除所有图表实例
  chartInstances.value.forEach(instance => instance.dispose())
  if (previewChartInstance) {
    previewChartInstance.dispose()
  }
})
</script>

<style scoped>
.dashboard-editor {
  padding: 20px;
}

.dashboard-form {
  max-width: 1200px;
  margin: 0 auto;
}

.charts-container {
  display: flex;
  gap: 20px;
}

.charts-list {
  flex: 1;
}

.charts-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.chart-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.size-input {
  width: 90px;
  margin-right: 10px;
}

.layout-preview {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
}

.preview-container {
  margin-top: 15px;
  min-height: 400px;
}

.layout-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 10px;
}

.layout-flex {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chart-item {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.chart-header {
  padding: 8px;
  border-bottom: 1px solid #dcdfe6;
  background-color: #f5f7fa;
}

.chart-content {
  height: calc(100% - 37px);
  min-height: 150px;
}

.chart-preview {
  height: 500px;
}
</style>