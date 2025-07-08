import DashboardList from '@/views/data-viz/DashboardList.vue'
import DashboardEditor from '@/views/data-viz/DashboardEditor.vue'
import DashboardDetail from '@/views/data-viz/DashboardDetail.vue'
import ChartList from '@/views/data-viz/ChartList.vue'
import ChartEditor from '@/views/data-viz/ChartEditor.vue'
import ChartDetail from '@/views/data-viz/ChartDetail.vue'
import DataSourceList from '@/views/data-viz/DataSourceList.vue'
import DataSourceEditor from '@/views/data-viz/DataSourceEditor.vue'

export default [
  {
    path: '',
    children: [
      {
        path: 'dashboards',
        name: 'DashboardList',
        component: DashboardList,
        meta: {
          title: '仪表盘列表',
          requiresAuth: true
        }
      },
      {
        path: 'dashboard/new',
        name: 'CreateDashboard',
        component: DashboardEditor,
        meta: {
          title: '新建仪表盘',
          requiresAuth: true
        }
      },
      {
        path: 'dashboard/:id',
        name: 'DashboardDetail',
        component: DashboardDetail,
        meta: {
          title: '仪表盘详情',
          requiresAuth: true
        }
      },
      {
        path: 'dashboard/:id/edit',
        name: 'EditDashboard',
        component: DashboardEditor,
        meta: {
          title: '编辑仪表盘',
          requiresAuth: true
        }
      },
      {
        path: 'charts',
        name: 'ChartList',
        component: ChartList,
        meta: {
          title: '图表列表',
          requiresAuth: true
        }
      },
      {
        path: 'chart/new',
        name: 'CreateChart',
        component: ChartEditor,
        meta: {
          title: '新建图表',
          requiresAuth: true
        }
      },
      {
        path: 'chart/:id',
        name: 'ChartDetail',
        component: ChartDetail,
        meta: {
          title: '图表详情',
          requiresAuth: true
        }
      },
      {
        path: 'chart/:id/edit',
        name: 'EditChart',
        component: ChartEditor,
        meta: {
          title: '编辑图表',
          requiresAuth: true
        }
      },
      {
        path: 'data-sources',
        name: 'DataSourceList',
        component: DataSourceList,
        meta: {
          title: '数据源管理',
          requiresAuth: true
        }
      },
      {
        path: 'data-source/new',
        name: 'CreateDataSource',
        component: DataSourceEditor,
        meta: {
          title: '新建数据源',
          requiresAuth: true
        }
      },
      {
        path: 'data-source/:id/edit',
        name: 'EditDataSource',
        component: DataSourceEditor,
        meta: {
          title: '编辑数据源',
          requiresAuth: true
        }
      }
    ]
  }
]