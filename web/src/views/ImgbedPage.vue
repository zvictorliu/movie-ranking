<template>
  <div class="imgbed-container">
    <div class="imgbed-header">
      <h1>图床管理</h1>
      <p>查看和管理图床中的所有图片</p>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索图片名称..."
          clearable
          @input="filterImages"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="toolbar-actions">
        <el-button type="primary" @click="refreshImages">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <span class="image-count">共 {{ filteredImages.length }} 张图片</span>
      </div>
    </div>

    <!-- 图片网格 -->
    <div v-if="filteredImages.length > 0" class="images-grid">
      <div v-for="image in paginatedImages" :key="image.filename" class="image-card">
        <div class="image-preview" @click="previewImage(image)">
          <el-image
            :src="image.path"
            :alt="image.filename"
            fit="cover"
            lazy
            class="thumbnail"
          >
            <template #error>
              <div class="image-error">
                <el-icon><Picture /></el-icon>
                <span>加载失败</span>
              </div>
            </template>
          </el-image>
        </div>
        <div class="image-info">
          <div class="image-filename" :title="image.filename">{{ image.filename }}</div>
          <div class="image-meta">
            <span class="image-size">{{ formatSize(image.size) }}</span>
            <span class="image-date">{{ formatDate(image.modified_time) }}</span>
          </div>
          <div class="image-actions">
            <el-button type="primary" size="small" class="copy-button" @click="copyShortcut(image)">
              <el-icon><CopyDocument /></el-icon>
              复制引用
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredImages.length === 0 && !loading" class="empty-state">
      <el-empty description="暂无图片" />
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredImages.length"
        layout="prev, pager, next, jumper"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 图片预览对话框 -->
    <el-dialog v-model="previewDialogVisible" title="图片预览" width="80%" center>
      <div v-if="currentPreviewImage" class="preview-content">
        <el-image :src="currentPreviewImage.path" :alt="currentPreviewImage.filename" fit="contain">
          <template #error>
            <div class="image-error-large">
              <el-icon><Picture /></el-icon>
              <span>图片加载失败</span>
            </div>
          </template>
        </el-image>
        <div class="preview-info">
          <p><strong>文件名:</strong> {{ currentPreviewImage.filename }}</p>
          <p><strong>大小:</strong> {{ formatSize(currentPreviewImage.size) }}</p>
          <p><strong>修改时间:</strong> {{ formatDate(currentPreviewImage.modified_time) }}</p>
          <p><strong>路径:</strong> {{ currentPreviewImage.path }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { Search, Refresh, Picture, CopyDocument, Document, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'ImgbedPage',
  components: {
    Search,
    Refresh,
    Picture,
    CopyDocument,
    Document,
    Loading,
  },
  data() {
    return {
      images: [],
      filteredImages: [],
      searchQuery: '',
      loading: false,
      currentPage: 1,
      pageSize: 20,
      previewDialogVisible: false,
      currentPreviewImage: null,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredImages.length / this.pageSize)
    },
    paginatedImages() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredImages.slice(start, end)
    },
  },
  mounted() {
    this.fetchImages()
    // 监听图片上传事件
    this.$eventBus.on('image-uploaded', this.handleImageUploaded)
  },
  beforeUnmount() {
    this.$eventBus.off('image-uploaded', this.handleImageUploaded)
  },
  methods: {
    async fetchImages() {
      this.loading = true
      try {
        const response = await axios.get('/api/imgbed')
        if (response.data.success) {
          this.images = response.data.images
          this.filteredImages = this.images
        } else {
          ElMessage.error('获取图片列表失败')
        }
      } catch (error) {
        console.error('获取图片列表失败:', error)
        ElMessage.error('获取图片列表失败，请稍后再试')
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
      this.currentPage = 1
    },
    refreshImages() {
      this.fetchImages()
      ElMessage.success('刷新成功')
    },
    handleImageUploaded(data) {
      // 如果上传的是图床类型的图片，刷新列表
      if (data.type === 'imgbed') {
        this.fetchImages()
      }
    },
    previewImage(image) {
      this.currentPreviewImage = image
      this.previewDialogVisible = true
    },
    copyShortcut(image) {
      // 使用完整的文件名（含扩展名）作为 title
      const shortcut = `<img title="${image.filename}" />`
      this.copyToClipboard(shortcut)
      ElMessage.success('图片引用已复制到剪贴板')
    },
    copyToClipboard(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
      } else {
        // 降级方案
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
    formatSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
    },
    formatDate(timestamp) {
      const date = new Date(timestamp * 1000)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
    handlePageChange(page) {
      this.currentPage = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
  },
}
</script>

<style scoped>
.imgbed-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.imgbed-header {
  text-align: center;
  margin-bottom: 40px;
}

.imgbed-header h1 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #667eea;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
}

.imgbed-header p {
  font-size: 16px;
  color: #764ba2;
  font-weight: 500;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
  flex-wrap: wrap;
  padding: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 12px;
  border: 2px solid rgba(102, 126, 234, 0.15);
}

.search-box {
  flex: 1;
  min-width: 250px;
  max-width: 400px;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.image-count {
  color: #764ba2;
  font-size: 14px;
  font-weight: 500;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.image-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  transition: all 0.3s ease;
  border: 2px solid rgba(102, 126, 234, 0.15);
}

.image-card:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
  transform: translateY(-2px);
  border-color: #667eea;
}

.image-preview {
  width: 100%;
  height: 200px;
  cursor: pointer;
  overflow: hidden;
  background: #f5f5f5;
}

.thumbnail {
  width: 100%;
  height: 100%;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.image-info {
  padding: 15px;
}

.image-filename {
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.image-actions {
  display: flex;
  justify-content: center;
}

.copy-button {
  width: 100%;
  font-weight: 500;
  transition: all 0.3s ease;
}

.copy-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.copy-button .el-icon {
  margin-right: 4px;
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;
}

.loading-state .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 100%;
  overflow: hidden;
}

.preview-content .el-image {
  max-width: 100%;
  max-height: 50vh;
  margin-bottom: 20px;
}

.image-error-large {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #999;
}

.image-error-large .el-icon {
  font-size: 64px;
  margin-bottom: 15px;
}

.preview-info {
  width: 100%;
  max-width: 100%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  padding: 20px;
  border-radius: 8px;
  box-sizing: border-box;
  overflow: hidden;
  border: 2px solid rgba(102, 126, 234, 0.15);
}

.preview-info p {
  margin: 8px 0;
  color: #764ba2;
  word-break: break-all;
  overflow-wrap: break-word;
  font-size: 14px;
  line-height: 1.6;
}

.preview-info strong {
  color: #667eea;
  margin-right: 8px;
  white-space: nowrap;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .imgbed-container {
    padding: 15px;
  }

  .imgbed-header h1 {
    font-size: 24px;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .toolbar-actions {
    justify-content: space-between;
  }

  .images-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  .image-preview {
    height: 150px;
  }

  .preview-info {
    padding: 15px;
  }

  .preview-info p {
    font-size: 12px;
  }

  .preview-content .el-image {
    max-height: 40vh;
  }
}

/* 暗色主题 */
body.dark-mode .imgbed-header h1 {
  color: #a8b5f0;
}

body.dark-mode .imgbed-header p {
  color: #c8a5d8;
}

body.dark-mode .toolbar {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.3);
}

body.dark-mode .image-count {
  color: #c8a5d8;
}

body.dark-mode .image-card {
  background: #2c2c2c;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
  border-color: rgba(168, 181, 240, 0.3);
}

body.dark-mode .image-card:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  border-color: #a8b5f0;
}

body.dark-mode .image-preview {
  background: #1a1a1a;
}

body.dark-mode .image-filename {
  color: #a8b5f0;
}

body.dark-mode .image-meta {
  color: #c8a5d8;
}

body.dark-mode .preview-info {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.3);
}

body.dark-mode .preview-info p {
  color: #c8a5d8;
}

body.dark-mode .preview-info strong {
  color: #a8b5f0;
}

body.dark-mode .copy-button:hover {
  box-shadow: 0 2px 8px rgba(168, 181, 240, 0.4);
}
</style>
