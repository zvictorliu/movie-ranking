<template>
  <div>
    <!-- 触发按钮 -->
    <button class="sidebar-trigger" @click="toggleSidebar" :title="isOpen ? '关闭图片预览' : '打开图片预览'">
      <i class="fa-solid fa-images"></i>
    </button>

    <!-- 遮罩层 -->
    <div v-if="isOpen" class="sidebar-overlay" @click="closeSidebar"></div>

    <!-- 侧边栏 -->
    <div :class="['image-sidebar', { open: isOpen }]">
      <div class="sidebar-header">
        <h3>图库</h3>
        <button class="close-btn" @click="closeSidebar">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <!-- 搜索框 -->
      <div class="sidebar-search">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索图片..."
          @input="filterImages"
        />
        <i class="fa-solid fa-search"></i>
      </div>

      <!-- 图片统计 -->
      <div class="sidebar-stats">
        <span>共 {{ filteredImages.length }} 张图片</span>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="sidebar-loading">
        <i class="fa-solid fa-spinner fa-spin"></i>
        <span>加载中...</span>
      </div>

      <!-- 图片网格 -->
      <div v-else-if="filteredImages.length > 0" class="sidebar-images">
        <div
          v-for="image in filteredImages"
          :key="image.filename"
          class="sidebar-image-item"
          @click="copyImageReference(image)"
          :title="`点击复制: ${image.filename}`"
        >
          <img :src="image.path" :alt="image.filename" />
          <div class="image-name">{{ image.filename }}</div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="sidebar-empty">
        <i class="fa-solid fa-image"></i>
        <span>暂无图片</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ImageSidebar',
  data() {
    return {
      isOpen: false,
      images: [],
      filteredImages: [],
      searchQuery: '',
      loading: false,
    }
  },
  methods: {
    async toggleSidebar() {
      this.isOpen = !this.isOpen
      if (this.isOpen && this.images.length === 0) {
        await this.fetchImages()
      }
    },
    closeSidebar() {
      this.isOpen = false
    },
    async fetchImages() {
      this.loading = true
      try {
        const response = await axios.get('/api/imgbed')
        if (response.data.success) {
          this.images = response.data.images
          this.filteredImages = this.images
        } else {
          this.$message.error('获取图片列表失败')
        }
      } catch (error) {
        console.error('获取图片列表失败:', error)
        this.$message.error('获取图片列表失败')
      } finally {
        this.loading = false
      }
    },
    filterImages() {
      if (!this.searchQuery.trim()) {
        this.filteredImages = this.images
      } else {
        const query = this.searchQuery.toLowerCase()
        this.filteredImages = this.images.filter((image) =>
          image.filename.toLowerCase().includes(query)
        )
      }
    },
    copyImageReference(image) {
      const shortcut = `<img title="${image.filename}" />`
      this.copyToClipboard(shortcut)
      this.$message.success('图片引用已复制到剪贴板')
    },
    copyToClipboard(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
      } else {
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand('copy')
        document.body.removeChild(textarea)
      }
    },
  },
  mounted() {
    // 监听图片上传事件，刷新列表
    this.$eventBus.on('image-uploaded', (data) => {
      if (data.type === 'imgbed' && this.isOpen) {
        this.fetchImages()
      }
    })
  },
  beforeUnmount() {
    this.$eventBus.off('image-uploaded')
  },
}
</script>

<style scoped>
/* 触发按钮 */
.sidebar-trigger {
  position: fixed;
  right: 20px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 3000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.sidebar-trigger:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-hover);
}

/* 遮罩层 */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 3001;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 侧边栏 */
.image-sidebar {
  position: fixed;
  top: 0;
  width: 350px;
  height: 100vh;
  background: var(--card-bg);
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.15);
  z-index: 3002;
  transition: right 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 默认关闭状态 */
.image-sidebar:not(.open) {
  right: -100%;
}

.image-sidebar.open {
  right: 0;
}

/* 侧边栏头部 */
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 2px solid var(--border-light);
  background: var(--bg-gradient-light);
}

.sidebar-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.close-btn:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

/* 搜索框 */
.sidebar-search {
  position: relative;
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-light);
}

.sidebar-search input {
  width: 100%;
  padding: 10px 35px 10px 12px;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.sidebar-search input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.sidebar-search i {
  position: absolute;
  right: 32px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

/* 统计信息 */
.sidebar-stats {
  padding: 12px 20px;
  font-size: 13px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-secondary);
}

/* 加载状态 */
.sidebar-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-muted);
  gap: 12px;
}

.sidebar-loading i {
  font-size: 32px;
}

/* 图片网格 */
.sidebar-images {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-image-item {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  transition: all 0.2s ease;
  position: relative;
}

.sidebar-image-item:hover {
  transform: translateY(-2px);
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.sidebar-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 6px 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.sidebar-image-item:hover .image-name {
  opacity: 1;
}

/* 空状态 */
.sidebar-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-muted);
  gap: 12px;
}

.sidebar-empty i {
  font-size: 48px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .image-sidebar {
    width: 33.33%;
    min-width: 200px;
  }

  .sidebar-trigger {
    right: 15px;
    bottom: 70px;
    width: 50px;
    height: 50px;
    font-size: 20px;
  }

  .sidebar-header h3 {
    font-size: 16px;
  }

  .sidebar-search {
    padding: 12px 15px;
  }

  .sidebar-stats {
    padding: 10px 15px;
    font-size: 12px;
  }

  .sidebar-images {
    padding: 12px;
    gap: 10px;
  }

  .image-name {
    font-size: 10px;
    padding: 4px 6px;
  }
}
</style>
