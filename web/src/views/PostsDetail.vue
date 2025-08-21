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
        <h1 class="post-title">{{ post.title }}</h1>
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
      <div class="post-body">
        <div v-html="renderedContent" class="markdown-content"></div>
      </div>

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
} from '@element-plus/icons-vue'
import axios from 'axios'
import { marked } from 'marked'

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
  },
  data() {
    return {
      post: null,
      loading: true,
      relatedPosts: [],
    }
  },
  computed: {
    readingTime() {
      if (!this.post || !this.post.content) return 1
      const wordsPerMinute = 200
      const wordCount = this.post.content.split(/\s+/).length
      return Math.ceil(wordCount / wordsPerMinute)
    },
    renderedContent() {
      if (!this.post || !this.post.content) return ''
      return marked(this.post.content)
    },
  },
  methods: {
    async fetchPost() {
      try {
        const slug = this.$route.params.slug
        const response = await axios.get(`/api/posts/${slug}`)
        this.post = response.data.post
        this.fetchRelatedPosts()
      } catch (error) {
        console.error('获取文章详情失败:', error)
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
    goToPost(slug) {
      this.$router.push({ name: 'PostsDetail', params: { slug } })
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
      const tagColors = {
        介绍: 'info',
        电影: 'primary',
        博客: 'success',
        2024: 'warning',
        新片: 'danger',
        期待: 'info',
        好莱坞: 'primary',
        经典: 'success',
        推荐: 'warning',
        回顾: 'info',
        必看: 'danger',
      }
      return tagColors[tag] || 'info'
    },
    shareToWeibo() {
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
    this.fetchPost()
  },
  watch: {
    '$route.params.slug'() {
      this.loading = true
      this.fetchPost()
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

.post-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.3;
  font-weight: 700;
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

.markdown-content {
  line-height: 1.8;
  font-size: 1.05rem;
  color: #333;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 600;
}

.markdown-content h1 {
  font-size: 2rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.6rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3rem;
}

.markdown-content h3 {
  font-size: 1.3rem;
}

.markdown-content p {
  margin-bottom: 1.2rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1.2rem;
  padding-left: 2rem;
}

.markdown-content li {
  margin-bottom: 0.5rem;
}

.markdown-content blockquote {
  background: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 15px;
  margin: 1.5rem 0;
  font-style: italic;
  color: #555;
}

.markdown-content code {
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
}

.markdown-content pre {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
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

body.dark-mode .markdown-content {
  color: #e0e0e0;
}

body.dark-mode .markdown-content h1,
body.dark-mode .markdown-content h2,
body.dark-mode .markdown-content h3,
body.dark-mode .markdown-content h4,
body.dark-mode .markdown-content h5,
body.dark-mode .markdown-content h6 {
  color: #e0e0e0;
}

body.dark-mode .post-excerpt blockquote {
  background: #2d2d2d;
  color: #c0c0c0;
}

body.dark-mode .markdown-content blockquote {
  background: #2d2d2d;
  color: #c0c0c0;
}

body.dark-mode .markdown-content code {
  background: #404040;
  color: #e0e0e0;
}

body.dark-mode .markdown-content pre {
  background: #2d2d2d;
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
</style>
