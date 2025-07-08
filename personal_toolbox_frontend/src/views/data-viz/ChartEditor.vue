<template>
  <div class="chart-editor">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑图表' : '新建图表' }}</h2>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="chart-form"
    >
      <el-form-item label="图表名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入图表名称" />
      </el-form-item>

      <el-form-item label="图表类型" prop="type">
        <el-select v-model="form.type" placeholder="请选择图表类型">
          <el-option label="折线图" value="line" />
          <el-option label="柱状图" value="bar" />
          <el-option label="饼图" value="pie" />
          <el-option label="散点图" value="scatter" />
          <el-option label="雷达图" value="radar" />
        </el-select>
      </el-form-item>

      <el-form-item label="数据源" prop="dataSourceId">
        <el-select
          v-model="form.dataSourceId"
          placeholder="请选择数据源"
          @change="handleDataSourceChange"
        >
          <el-option
            v-for="source in dataSources"
            :key="source.id"
            :label="source.name"
            :value="source.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="数据查询" prop="query">
        <el-input
          v-model="form.query"
          type="textarea"
          :rows="4"
          placeholder="请输入数据查询语句"
        />
        <div class="query-actions">
          <el-button type="primary" @click="handleTestQuery">
            <el-icon><Connection /></el-icon>测试查询
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="图表配置" prop="options">
        <div class="chart-config">
          <div class="config-editor">
            <el-tabs v-model="activeConfigTab">
              <el-tab-pane label="基础配置" name="basic">
                <el-form-item label="标题" prop="options.title">
                  <el-input v-model="form.options.title" placeholder="请输入图表标题" />
                </el-form-item>

                <el-form-item label="子标题" prop="options.subtitle">
                  <el-input v-model="form.options.subtitle" placeholder="请输入图表子标题" />
                </el-form-item>

                <el-form-item label="图例显示" prop="options.legend">
                  <el-switch v-model="form.options.legend" />
                </el-form-item>

                <el-form-item label="工具箱" prop="options.toolbox">
                  <el-switch v-model="form.options.toolbox" />
                </el-form-item>
              </el-tab-pane>

              <el-tab-pane label="坐标轴" name="axis" v-if="showAxisConfig">
                <el-form-item label="X轴标题" prop="options.xAxis.name">
                  <el-input v-model="form.options.xAxis.name" placeholder="请输入X轴标题" />
                </el-form-item>

                <el-form-item label="Y轴标题" prop="options.yAxis.name">
                  <el-input v-model="form.options.yAxis.name" placeholder="请输入Y轴标题" />
                </el-form-item>
              </el-tab-pane>

              <el-tab-pane label="系列配置" name="series">
                <el-form-item label="系列名称" prop="options.series.name">
                  <el-input v-model="form.options.series.name" placeholder="请输入系列名称" />
                </el-form-item>

                <el-form-item label="数据标签" prop="options.series.label">
                  <el-switch v-model="form.options.series.label" />
                </el-form-item>
              </el-tab-pane>
            </el-tabs>
          </div>

          <div class="chart-preview">
            <div ref="chartPreview" class="preview-container"></div>
          </div>
        </div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '创建图表' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Connection } from '@element-plus/icons-vue'
import api from '@/api'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const chartPreview = ref(null)
let chartInstance = null

const isEdit = computed(() => route.params.id !== undefined)
const showAxisConfig = computed(() => ['line', 'bar', 'scatter'].includes(form.value.type))

const activeConfigTab = ref('basic')
const dataSources = ref([])

const form = ref({
  name: '',
  type: '',
  dataSourceId: '',
  query: '',
  options: {
    title: '',
    subtitle: '',
    legend: true,
    toolbox: true,
    xAxis: {
      name: ''
    },
    yAxis: {
      name: ''
    },
    series: {
      name: '',
      label: false
    }
  }
})

const rules = {
  name: [{ required: true, message: '请输入图表名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择图表类型', trigger: 'change' }],
  dataSourceId: [{ required: true, message: '请选择数据源', trigger: 'change' }],
  query: [{ required: true, message: '请输入数据查询语句', trigger: 'blur' }]
}

const fetchDataSources = async () => {
  try {
    const response = await api.dataViz.getDataSources()
    dataSources.value = response.data.results
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
  }
}

const fetchChartData = async () => {
  if (!isEdit.value) return

  try {
    const response = await api.dataViz.getChart(route.params.id)
    const chartData = response.data
    form.value = {
      name: chartData.name,
      type: chartData.type,
      dataSourceId: chartData.data_source_id,
      query: chartData.query,
      options: chartData.options
    }
    updateChartPreview()
  } catch (error) {
    ElMessage.error('获取图表数据失败')
  }
}

const handleDataSourceChange = () => {
  form.value.query = '' // 清空查询语句
}

const handleTestQuery = async () => {
  if (!form.value.dataSourceId || !form.value.query) {
    ElMessage.warning('请先选择数据源并输入查询语句')
    return
  }

  try {
    const response = await api.dataViz.testQuery({
      data_source_id: form.value.dataSourceId,
      query: form.value.query
    })
    
    // 更新图表预览
    updateChartPreview(response.data)
    ElMessage.success('查询测试成功')
  } catch (error) {
    ElMessage.error('查询测试失败：' + error.message)
  }
}

const updateChartPreview = (data) => {
  if (!chartInstance) {
    chartInstance = echarts.init(chartPreview.value)
  }

  const options = {
    title: {
      text: form.value.options.title,
      subtext: form.value.options.subtitle
    },
    legend: {
      show: form.value.options.legend
    },
    toolbox: {
      show: form.value.options.toolbox,
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: showAxisConfig.value ? {
      name: form.value.options.xAxis.name,
      type: 'category'
    } : undefined,
    yAxis: showAxisConfig.value ? {
      name: form.value.options.yAxis.name,
      type: 'value'
    } : undefined,
    series: [
      {
        name: form.value.options.series.name,
        type: form.value.type,
        label: {
          show: form.value.options.series.label
        },
        data: data || []
      }
    ]
  }

  chartInstance.setOption(options, true)
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    const chartData = {
      name: form.value.name,
      type: form.value.type,
      data_source_id: form.value.dataSourceId,
      query: form.value.query,
      options: form.value.options
    }

    if (isEdit.value) {
      await api.dataViz.updateChart(route.params.id, chartData)
      ElMessage.success('图表更新成功')
    } else {
      await api.dataViz.createChart(chartData)
      ElMessage.success('图表创建成功')
    }

    router.push('/data-viz/charts')
  } catch (error) {
    if (error.name === 'ValidationError') return
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const handleCancel = () => {
  router.back()
}

// 监听窗口大小变化，重绘图表
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  fetchDataSources()
  fetchChartData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.chart-editor {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.chart-form {
  max-width: 1200px;
}

.query-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

.chart-config {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 10px;
}

.config-editor {
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  padding: 20px;
}

.chart-preview {
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  padding: 20px;
}

.preview-container {
  height: 400px;
}

:deep(.el-tabs__content) {
  padding: 20px 0;
}
</style>