import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    // 当前主题：'gradient' (渐变紫色) 或 'minimal' (简洁黑白)
    currentTheme: localStorage.getItem('app-theme') || 'gradient',
    // 暗色模式：true 或 false
    darkMode: localStorage.getItem('dark-mode') === 'true' || false,
  }),

  getters: {
    isGradientTheme: (state) => state.currentTheme === 'gradient',
    isMinimalTheme: (state) => state.currentTheme === 'minimal',
    themeClass: (state) => `theme-${state.currentTheme}`,
  },

  actions: {
    // 切换主题
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'gradient' ? 'minimal' : 'gradient'
      localStorage.setItem('app-theme', this.currentTheme)
      this.applyTheme()
    },

    // 设置特定主题
    setTheme(theme) {
      if (theme === 'gradient' || theme === 'minimal') {
        this.currentTheme = theme
        localStorage.setItem('app-theme', theme)
        this.applyTheme()
      }
    },

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

      // 移除旧的主题类
      body.classList.remove('theme-gradient', 'theme-minimal', 'dark-mode')

      // 添加新的主题类
      body.classList.add(`theme-${this.currentTheme}`)

      // 添加暗色模式类
      if (this.darkMode) {
        body.classList.add('dark-mode')
      }
    },

    // 初始化主题
    initTheme() {
      this.applyTheme()
    },
  },
})
