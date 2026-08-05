import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    // 暗色模式：true 或 false
    darkMode: localStorage.getItem('dark-mode') === 'true' || false,
  }),

  actions: {
    // 切换暗色模式
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('dark-mode', this.darkMode)
      this.applyTheme()
    },

    // 设置暗色模式
    setDarkMode(enabled) {
      this.darkMode = enabled
      localStorage.setItem('dark-mode', enabled)
      this.applyTheme()
    },

    // 应用主题到 DOM
    applyTheme() {
      const body = document.body

      // 添加/移除暗色模式类
      body.classList.toggle('dark-mode', this.darkMode)
    },

    // 初始化主题
    initTheme() {
      this.applyTheme()
    },
  },
})
