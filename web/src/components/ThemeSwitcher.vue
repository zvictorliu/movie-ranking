<template>
  <div class="theme-switcher">
    <div class="theme-selector">
      <button
        @click="setTheme('gradient')"
        :class="{ active: themeStore.isGradientTheme }"
        class="theme-button"
        title="渐变紫色主题"
      >
        <span class="material-icons">gradient</span>
        <span class="theme-name">渐变</span>
      </button>
      <button
        @click="setTheme('minimal')"
        :class="{ active: themeStore.isMinimalTheme }"
        class="theme-button"
        title="简洁黑白主题"
      >
        <span class="material-icons">contrast</span>
        <span class="theme-name">简洁</span>
      </button>
    </div>
  </div>
</template>

<script>
import { useThemeStore } from '../store/theme'

export default {
  name: 'ThemeSwitcher',
  setup() {
    const themeStore = useThemeStore()
    return { themeStore }
  },
  methods: {
    setTheme(theme) {
      this.themeStore.setTheme(theme)
      this.$emit('theme-changed', theme)
    },
  },
}
</script>

<style scoped>
.theme-switcher {
  display: inline-flex;
  align-items: center;
}

.theme-selector {
  display: flex;
  gap: 8px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.theme-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.theme-button:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.theme-button.active {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.theme-button .material-icons {
  font-size: 18px;
}

.theme-name {
  font-size: 13px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .theme-name {
    display: none;
  }

  .theme-button {
    padding: 8px;
  }
}

</style>

<style>
/* 简洁主题下的样式调整（非 scoped） */
/* 亮色模式 */
body.theme-minimal:not(.dark-mode) .theme-selector {
  background: rgba(0, 0, 0, 0.08);
}

body.theme-minimal:not(.dark-mode) .theme-button {
  color: #333333;
}

body.theme-minimal:not(.dark-mode) .theme-button:hover {
  background: rgba(0, 0, 0, 0.1);
}

body.theme-minimal:not(.dark-mode) .theme-button.active {
  background: rgba(0, 0, 0, 0.15);
}

/* 暗色模式 */
body.theme-minimal.dark-mode .theme-selector {
  background: rgba(255, 255, 255, 0.08);
}

body.theme-minimal.dark-mode .theme-button {
  color: #e0e0e0;
}

body.theme-minimal.dark-mode .theme-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

body.theme-minimal.dark-mode .theme-button.active {
  background: rgba(255, 255, 255, 0.15);
}
</style>
