<template>
  <div class="dashboard-list">
    <div class="page-header">
      <h2>仪表盘列表</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建仪表盘
      </el-button>
    </div>

    <el-row :gutter="20" class="dashboard-grid">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="dashboard in dashboards" :key="dashboard.id">
        <el-card class="dashboard-card" :body-style="{ padding: '0' }">
          <div class="dashboard-preview">
            <!-- 预览图 -->
          </div>
          <div class="dashboard-info">
            <h3>{{ dashboard.name }}</h3>
            <p>{{ dashboard.description }}</p>
            <div class="dashboard-actions">
              <el-button-group>
                <el-button type="primary" @click="handleView(dashboard.id)">
                  <el-icon><View /></el-icon>查看
                </el-button>
                <el-button type="primary" @click="handleEdit(dashboard.id)">
                  <el-icon><Edit /></el-icon>编辑
                </el-button>
                <el-button type="danger" @click="handleDelete(dashboard.id)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </el-button-group>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-pagination
      v-if="total > 0"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[12, 24, 36, 48]"
      layout="total, sizes, prev, pager, next"
      class="pagination"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, View, Edit, Delete } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const dashboards = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

const fetchDashboards = async () => {
  try {
    const response = await api.dataViz.getDashboards({
      page: currentPage.value,
      page_size: pageSize.value
    })
    dashboards.value = response.data.results
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取仪表盘列表失败')
  }
}

const handleCreate = () => {
  router.push('/data-viz/dashboard/new')
}

const handleView = (id) => {
  router.push(`/data-viz/dashboard/${id}`)
}

const handleEdit = (id) => {
  router.push(`/data-viz/dashboard/${id}/edit`)
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个仪表盘吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.dataViz.deleteDashboard(id)
    ElMessage.success('删除成功')
    await fetchDashboards()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchDashboards()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchDashboards()
}

onMounted(() => {
  fetchDashboards()
})
</script>

<style scoped>
.dashboard-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-grid {
  margin-bottom: 20px;
}

.dashboard-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.dashboard-preview {
  height: 160px;
  background-color: #f5f7fa;
}

.dashboard-info {
  padding: 14px;
}

.dashboard-info h3 {
  margin: 0 0 10px;
  font-size: 16px;
}

.dashboard-info p {
  margin: 0 0 15px;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.dashboard-actions {
  display: flex;
  justify-content: flex-end;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>