import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'

// 导入共享样式
import './styles/article-title.scss'
// 导入主题样式
import './assets/themes.css'

// 创建 Vue 应用实例
const app = createApp(App)

// 创建 Pinia 实例
const pinia = createPinia()

// 创建全局事件总线
const eventBus = {
  events: {},
  emit(event, data) {
    if (this.events[event]) {
      this.events[event].forEach((callback) => callback(data))
    }
  },
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = []
    }
    this.events[event].push(callback)
  },
  off(event, callback) {
    if (this.events[event]) {
      this.events[event] = this.events[event].filter((cb) => cb !== callback)
    }
  },
}

// 将事件总线挂载到全局
app.config.globalProperties.$eventBus = eventBus

app.use(ElementPlus)
app.use(router)
app.use(pinia)

// 初始化主题
import { useThemeStore } from './store/theme'
const themeStore = useThemeStore()
themeStore.initTheme()

// 挂载应用
app.mount('#app')
