import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'

// 导入共享样式
import './styles/article-title.scss'

// 创建 Vue 应用实例
const app = createApp(App)

// 创建 Pinia 实例
const pinia = createPinia()

app.use(ElementPlus)
app.use(router)
app.use(pinia)

// 挂载应用
app.mount('#app')
