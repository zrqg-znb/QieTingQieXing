import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

// 导入全局样式
import './assets/styles/global.scss'

// 创建Vue应用实例
const app = createApp(App)

// 使用Pinia状态管理
app.use(createPinia())

// 使用Vue Router
app.use(router)

// 使用Element Plus
app.use(ElementPlus, { size: 'default' })

// 挂载应用
app.mount('#app')