<template>
  <div class="post-detail-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <!-- 文章内容 -->
    <div v-else-if="post" class="post-content">
      <!-- 返回按钮 -->
      <div class="back-button">
        <el-button @click="goBack" type="primary" plain>
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
      </div>

      <!-- 文章头部 -->
      <div class="post-header">
        <div class="title-container">
          <h1>{{ post.title }}</h1>
          <div class="edit-buttons">
            <el-tooltip content="编辑文章信息" placement="top">
              <button @click="openEditMetaDialog" class="edit-meta-button">
                <el-icon><Setting /></el-icon>
                <span class="button-text">信息</span>
              </button>
            </el-tooltip>
            <el-tooltip content="编辑正文内容" placement="top">
              <button @click="openEditBodyDialog" class="edit-body-button">
                <el-icon><Document /></el-icon>
                <span class="button-text">正文</span>
              </button>
            </el-tooltip>
          </div>
        </div>
        <div class="post-meta">
          <div class="meta-item">
            <el-icon><Calendar /></el-icon>
            <span>{{ formatDate(post.date) }}</span>
          </div>
          <div class="meta-item">
            <el-icon><User /></el-icon>
            <span>{{ post.author }}</span>
          </div>
          <div class="meta-item">
            <el-icon><Clock /></el-icon>
            <span>阅读时间: {{ readingTime }} 分钟</span>
          </div>
        </div>

        <!-- 标签 -->
        <div class="post-tags">
          <el-tag
            v-for="tag in post.tags"
            :key="tag"
            :type="getTagType(tag)"
            effect="plain"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- 文章摘要 -->
      <div v-if="post.excerpt" class="post-excerpt">
        <blockquote>
          {{ post.excerpt }}
        </blockquote>
      </div>

      <!-- 文章正文 -->
      <div class="post-body" v-if="!editBodyDialogVisible">
        <MarkdownRender :content="post.content" />
      </div>

      <!-- 编辑正文对话框 -->
      <el-dialog
        v-model="editBodyDialogVisible"
        title="编辑正文内容"
        width="90%"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        class="body-editor-dialog"
      >
        <LiveEditor
          v-if="post"
          v-model="post.content"
          :title="`编辑《${post.title}》正文`"
          :post-slug="post.slug"
          @saved="onBodySaved"
          @cancelled="editBodyDialogVisible = false"
        />
      </el-dialog>

      <!-- 文章底部 -->
      <div class="post-footer">
        <div class="share-section">
          <h3>分享文章</h3>
          <div class="share-buttons">
            <el-button @click="shareToWeibo" type="danger" size="small">
              <el-icon><Share /></el-icon>
              微博
            </el-button>
            <el-button @click="shareToWeChat" type="success" size="small">
              <el-icon><ChatDotRound /></el-icon>
              微信
            </el-button>
            <el-button @click="copyLink" type="primary" size="small">
              <el-icon><LinkIcon /></el-icon>
              复制链接
            </el-button>
          </div>
        </div>

        <!-- 相关文章 -->
        <div v-if="relatedPosts.length > 0" class="related-posts">
          <h3>相关文章</h3>
          <div class="related-posts-list">
            <div
              v-for="relatedPost in relatedPosts"
              :key="relatedPost.slug"
              class="related-post-item"
              @click="goToPost(relatedPost.slug)"
            >
              <h4>{{ relatedPost.title }}</h4>
              <p>{{ relatedPost.excerpt }}</p>
              <span class="related-post-date">{{ formatDate(relatedPost.date) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-container">
      <el-result icon="error" title="文章未找到" sub-title="抱歉，您访问的文章不存在或已被删除">
        <template #extra>
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </template>
      </el-result>
    </div>

    <!-- 编辑元信息对话框 -->
    <MetaEditor
      v-if="post"
      v-model:visible="editMetaDialogVisible"
      type="post"
      :data="post"
      :id="post.slug"
      @saved="onMetaSaved"
      @cancelled="editMetaDialogVisible = false"
    />
  </div>
</template>

<script>
import {
  ArrowLeft,
  Calendar,
  User,
  Clock,
  Share,
  ChatDotRound,
  Link as LinkIcon,
  Document,
  Setting,
} from '@element-plus/icons-vue'
import axios from 'axios'
import LiveEditor from '@/components/LiveEditor.vue'
import MetaEditor from '@/components/MetaEditor.vue'
import MarkdownRender from '@/components/MarkdownRender.vue'

export default {
  name: 'PostsDetail',
  components: {
    ArrowLeft,
    Calendar,
    User,
    Clock,
    Share,
    ChatDotRound,
    LinkIcon,
    Document,
    Setting,
    LiveEditor,
    MetaEditor,
    MarkdownRender,
  },
  data() {
    return {
      post: null,
      loading: true,
      relatedPosts: [],
      editBodyDialogVisible: false, // 控制编辑正文对话框的显示状态
      editMetaDialogVisible: false, // 控制编辑元信息对话框的显示状态
    }
  },
  computed: {
    readingTime() {
      if (!this.post || !this.post.content) return 1
      const wordsPerMinute = 200
      const wordCount = this.post.content.split(/\s+/).length
      return Math.ceil(wordCount / wordsPerMinute)
    },
  },
  methods: {
    async fetchPost() {
      try {
        const slug = this.$route.params.slug
        console.log('fetchPost called with slug:', slug)

        if (!slug) {
          console.error('Slug parameter is missing')
          this.$message.error('文章标识符缺失')
          return
        }

        const response = await axios.get(`/api/posts/${slug}`)
        console.log('API response:', response.data)

        if (response.data && response.data.post) {
          this.post = response.data.post
          console.log('Post loaded successfully:', this.post.title)
          this.fetchRelatedPosts()
        } else {
          console.error('Invalid API response format')
          this.$message.error('文章数据格式错误')
        }
      } catch (error) {
        console.error('获取文章详情失败:', error)
        if (error.response && error.response.status === 404) {
          this.$message.error('文章不存在')
        } else {
          this.$message.error('获取文章失败，请稍后重试')
        }
      } finally {
        this.loading = false
      }
    },
    async fetchRelatedPosts() {
      // 模拟相关文章数据
      const response = await axios.get('/api/posts')
      const allPosts = response.data.posts || []

      // 根据当前文章的标签找到相关文章
      const currentSlug = this.post.slug
      this.relatedPosts = allPosts.filter((post) => post.slug !== currentSlug).slice(0, 2) // 只显示2篇相关文章
    },
    goBack() {
      this.$router.push({ name: 'PostsPage' })
    },
    openEditBodyDialog() {
      this.editBodyDialogVisible = true // 打开编辑正文对话框
    },
    openEditMetaDialog() {
      this.editMetaDialogVisible = true
    },
    onMetaSaved() {
      // 刷新整个页面以显示更新后的信息
      location.reload()
    },
    async onBodySaved(newBody) {
      // 更新本地数据
      this.post.content = newBody
      this.editBodyDialogVisible = false
    },
    goToPost(slug) {
      this.$router.push({ name: 'PostsDetail', params: { slug } })
    },

    async goToDetail(id) {
      try {
        this.$router.push({ name: 'MovieDetail', params: { id } })
      } catch (error) {
        console.error('电影记录不存在:', error)
        this.$message.error('不存在对应的电影记录')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    },
    getTagType(tag) {
      // 根据标签名字生成固定的类型映射 [[6]]
      const types = ['success', 'info', 'warning', 'danger']
      const typeIndex = Math.abs(this.hashCode(tag)) % types.length
      return types[typeIndex]
    },
    hashCode(str) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }
      return hash
    },
    shareToWeibo() {
      if (!this.post) return
      const url = encodeURIComponent(window.location.href)
      const title = encodeURIComponent(this.post.title)
      window.open(`https://service.weibo.com/share/share.php?url=${url}&title=${title}`)
    },
    shareToWeChat() {
      this.$message.info('请使用微信扫描二维码分享')
    },
    async copyLink() {
      try {
        await navigator.clipboard.writeText(window.location.href)
        this.$message.success('链接已复制到剪贴板')
      } catch {
        this.$message.error('复制失败，请手动复制')
      }
    },
  },
  mounted() {
    console.log('PostsDetail mounted, route params:', this.$route.params)
    this.fetchPost()
  },
  watch: {
    '$route.params.slug'(newSlug, oldSlug) {
      console.log('Route slug changed:', { newSlug, oldSlug })
      if (newSlug !== oldSlug) {
        this.loading = true
        this.post = null // 重置 post 数据
        this.fetchPost()
      }
    },
  },
}
</script>

<style scoped>
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  padding: 40px 20px;
}

.back-button {
  margin-bottom: 30px;
}

.post-header {
  margin-bottom: 40px;
  text-align: center;
}

/* title-container 基础样式已移至 article-title.scss */

/* 编辑按钮样式已移至 article-title.scss */

/* 编辑正文对话框样式 */
:deep(.body-editor-dialog .el-dialog) {
  height: 90vh;
}

:deep(.body-editor-dialog .el-dialog__body) {
  height: calc(90vh - 120px);
  padding: 0;
}

.post-meta {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 0.95rem;
}

.post-tags {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  font-size: 0.9rem;
}

.post-excerpt {
  margin-bottom: 40px;
}

.post-excerpt blockquote {
  background: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 20px;
  margin: 0;
  font-style: italic;
  color: #555;
  font-size: 1.1rem;
  line-height: 1.6;
}

.post-body {
  margin-bottom: 60px;
}

.post-footer {
  border-top: 1px solid #eee;
  padding-top: 40px;
}

.share-section {
  margin-bottom: 40px;
}

.share-section h3 {
  margin-bottom: 15px;
  color: #333;
}

.share-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.related-posts h3 {
  margin-bottom: 20px;
  color: #333;
}

.related-posts-list {
  display: grid;
  gap: 20px;
}

.related-post-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.related-post-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.related-post-item h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.related-post-item p {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
  line-height: 1.5;
}

.related-post-date {
  color: #999;
  font-size: 0.8rem;
}

.error-container {
  padding: 60px 20px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-detail-container {
    padding: 15px;
  }

  .post-title {
    font-size: 2rem;
  }

  .post-meta {
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }

  .share-buttons {
    justify-content: center;
  }

  .related-posts-list {
    grid-template-columns: 1fr;
  }
}

/* 暗色模式支持 */
body.dark-mode .post-detail-container {
  background-color: #1a1a1a;
  color: #e0e0e0;
}

body.dark-mode .post-title {
  color: #e0e0e0;
}

body.dark-mode .meta-item {
  color: #b0b0b0;
}

body.dark-mode .post-excerpt blockquote {
  background: #2d2d2d;
  color: #c0c0c0;
}

body.dark-mode .related-post-item {
  background: #2d2d2d;
  border-color: #404040;
  color: #e0e0e0;
}

body.dark-mode .related-post-item:hover {
  background: #404040;
}

body.dark-mode .related-post-item h4 {
  color: #e0e0e0;
}

body.dark-mode .related-post-item p {
  color: #b0b0b0;
}

body.dark-mode .related-post-date {
  color: #808080;
}

/* 电影卡片shortcode样式 - 与ActorDetail保持一致 */
.movie-card-shortcode {
  margin: 2rem 0;
}

.movie-card-content {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

.movie-cover-wrapper {
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.movie-cover-wrapper:hover {
  transform: scale(1.05);
}

.movie-cover {
  max-width: 350px;
  object-fit: cover;
  aspect-ratio: 16 / 9;
  margin-right: 20px;
}

.movie-details {
  flex: 1;
  text-align: left;
}

.movie-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px 0;
}

.rating {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-bottom: 10px;
}

.rating strong {
  color: #666;
  font-size: 0.9rem;
  margin-right: 5px;
}

.stars {
  display: flex;
  align-items: center;
  gap: 2px;
}

.stars .material-icons {
  font-size: 20px;
  color: #ccc;
}

.stars .material-icons.filled {
  color: #ffca28;
}

.movie-description {
  color: #555;
  line-height: 1.5;
  margin: 0 0 10px 0;
  font-size: 0.9rem;
}

.movie-actors {
  color: #666;
  font-size: 0.9rem;
}

.movie-actors strong {
  color: #333;
}

.movie-not-found {
  padding: 20px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  color: #666;
  text-align: center;
  font-style: italic;
}

/* 宽屏设备：横向排列 */
@media (min-width: 768px) {
  .movie-card-content {
    flex-direction: row;
  }
  .movie-cover {
    max-width: 350px;
    object-fit: cover;
    aspect-ratio: 16 / 9;
    margin-right: 20px;
  }
  .movie-details {
    flex: 1;
    text-align: left;
  }
}

/* 窄屏设备：竖向排列 */
@media (max-width: 768px) {
  .movie-card-content {
    flex-direction: column;
    align-items: flex-start;
  }
  .movie-cover {
    max-width: 100%;
    margin-right: 0;
    margin-bottom: 10px;
  }
  .movie-details {
    width: 100%;
    text-align: left;
  }
}

/* 暗色模式支持 */
body.dark-mode .movie-card-content {
  border-color: #404040;
  background-color: #2d2d2d;
}

body.dark-mode .movie-title {
  color: #e0e0e0;
}

body.dark-mode .rating strong {
  color: #b0b0b0;
}

body.dark-mode .movie-description {
  color: #c0c0c0;
}

body.dark-mode .movie-actors {
  color: #b0b0b0;
}

body.dark-mode .movie-actors strong {
  color: #e0e0e0;
}

body.dark-mode .movie-not-found {
  background-color: #2d2d2d;
  border-color: #404040;
  color: #b0b0b0;
}
</style>
