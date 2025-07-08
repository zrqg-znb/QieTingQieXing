import request from '@/utils/request'

// 仪表盘相关接口
export const getDashboards = () => {
  return request({
    url: '/api/data-viz/dashboards/',
    method: 'get'
  })
}

export const getDashboard = (id) => {
  return request({
    url: `/api/data-viz/dashboards/${id}/`,
    method: 'get'
  })
}

export const createDashboard = (data) => {
  return request({
    url: '/api/data-viz/dashboards/',
    method: 'post',
    data
  })
}

export const updateDashboard = (id, data) => {
  return request({
    url: `/api/data-viz/dashboards/${id}/`,
    method: 'put',
    data
  })
}

export const deleteDashboard = (id) => {
  return request({
    url: `/api/data-viz/dashboards/${id}/`,
    method: 'delete'
  })
}

// 图表相关接口
export const getCharts = (params) => {
  return request({
    url: '/api/data-viz/charts/',
    method: 'get',
    params
  })
}

export const getChart = (id) => {
  return request({
    url: `/api/data-viz/charts/${id}/`,
    method: 'get'
  })
}

export const getChartData = (id) => {
  return request({
    url: `/api/data-viz/charts/${id}/data/`,
    method: 'get'
  })
}

export const getChartUsage = (id) => {
  return request({
    url: `/api/data-viz/charts/${id}/usage/`,
    method: 'get'
  })
}

export const createChart = (data) => {
  return request({
    url: '/api/data-viz/charts/',
    method: 'post',
    data
  })
}

export const updateChart = (id, data) => {
  return request({
    url: `/api/data-viz/charts/${id}/`,
    method: 'put',
    data
  })
}

export const deleteChart = (id) => {
  return request({
    url: `/api/data-viz/charts/${id}/`,
    method: 'delete'
  })
}

export const previewChart = (data) => {
  return request({
    url: '/api/data-viz/charts/preview/',
    method: 'post',
    data
  })
}

// 数据源相关接口
export const getDataSources = () => {
  return request({
    url: '/api/data-viz/data-sources/',
    method: 'get'
  })
}

export const getDataSource = (id) => {
  return request({
    url: `/api/data-viz/data-sources/${id}/`,
    method: 'get'
  })
}

export const getDataSourceUsage = (id) => {
  return request({
    url: `/api/data-viz/data-sources/${id}/usage/`,
    method: 'get'
  })
}

export const createDataSource = (data) => {
  return request({
    url: '/api/data-viz/data-sources/',
    method: 'post',
    data
  })
}

export const updateDataSource = (id, data) => {
  return request({
    url: `/api/data-viz/data-sources/${id}/`,
    method: 'put',
    data
  })
}

export const deleteDataSource = (id) => {
  return request({
    url: `/api/data-viz/data-sources/${id}/`,
    method: 'delete'
  })
}

export const testDataSourceConnection = (id) => {
  return request({
    url: `/api/data-viz/data-sources/${id}/test-connection/`,
    method: 'post'
  })
}

export const testNewDataSourceConnection = (data) => {
  return request({
    url: '/api/data-viz/data-sources/test-connection/',
    method: 'post',
    data
  })
}

export const testChartQuery = (data) => {
  return request({
    url: '/api/data-viz/charts/test-query/',
    method: 'post',
    data
  })
}