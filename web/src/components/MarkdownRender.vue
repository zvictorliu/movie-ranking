<template>
  <div class="markdown-render">
    <template v-for="(item, index) in parsedContent" :key="index">
      <!-- 如果是 MoviePreview 组件 -->
      <MoviePreview v-if="item.type === 'movie-preview'" :title="item.movieTitle" />
      <!-- 如果是图片 -->
      <img
        v-else-if="item.type === 'image'"
        :src="getImageSrc(item.imageTitle)"
        :alt="item.imageTitle"
        class="markdown-inline-image"
      />
      <!-- 如果是普通 HTML 内容 -->
      <div v-else v-html="item.content" class="markdown-content"></div>
    </template>
  </div>
</template>

<script>
import { marked } from 'marked'
import MoviePreview from '@/components/MoviePreview.vue'

export default {
  name: 'MarkdownRender',
  components: {
    MoviePreview,
  },
  props: {
    content: {
      type: String,
      required: true,
    },
  },
  computed: {
    parsedContent() {
      if (!this.content) return []

      // 先使用 marked 渲染 markdown
      let renderedHtml = marked(this.content)

      // 替换图片路径为绝对路径（全局替换）
      renderedHtml = renderedHtml.replace(/src="\.\/imgs/g, 'src="/imgs')

      // 解析 HTML 内容，分离自定义组件和普通内容
      const contentItems = []
      const customShortcutRegex = /<(movie|img)\s+title=["']([^"']+)["']\s*\/?>/g
      let lastIndex = 0
      let match

      while ((match = customShortcutRegex.exec(renderedHtml)) !== null) {
        // 添加自定义标签之前的普通内容
        if (match.index > lastIndex) {
          const htmlContent = renderedHtml.substring(lastIndex, match.index)
          if (htmlContent.trim()) {
            contentItems.push({
              type: 'html',
              content: htmlContent,
            })
          }
        }

        const tagType = match[1]
        const tagTitle = match[2]

        if (tagType === 'movie') {
          contentItems.push({
            type: 'movie-preview',
            movieTitle: tagTitle,
          })
        } else if (tagType === 'img') {
          contentItems.push({
            type: 'image',
            imageTitle: tagTitle,
          })
        }

        lastIndex = match.index + match[0].length
      }

      // 添加最后剩余的普通内容
      if (lastIndex < renderedHtml.length) {
        const htmlContent = renderedHtml.substring(lastIndex)
        if (htmlContent.trim()) {
          contentItems.push({
            type: 'html',
            content: htmlContent,
          })
        }
      }

      return contentItems
    },
  },
  methods: {
    getImageSrc(title) {
      return `/imgs/imgbed/${encodeURIComponent(title)}`
    },
  },
}
</script>

<style scoped>
.markdown-render {
  color: var(--text-primary);
}

.markdown-content {
  line-height: 1.8;
  font-size: 1.05rem;
  color: var(--text-primary);
}

.markdown-inline-image {
  max-width: 100%;
  display: block;
  margin: 1.5rem auto;
  border-radius: 8px;
}

/* 标题样式 */
.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-weight: 600;
  line-height: 1.3;
}

.markdown-content :deep(h1) {
  font-size: 2rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.markdown-content :deep(h2) {
  font-size: 1.6rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3rem;
}

.markdown-content :deep(h3) {
  font-size: 1.3rem;
}

.markdown-content :deep(h4) {
  font-size: 1.1rem;
}

.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  font-size: 1rem;
}

/* 段落和文本样式 */
.markdown-content :deep(p) {
  margin-bottom: 1.2rem;
  line-height: 1.8;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: var(--text-accent);
}

.markdown-content :deep(em) {
  font-style: italic;
  color: var(--text-secondary);
}

/* 列表样式 */
.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin-bottom: 1.2rem;
  padding-left: 2rem;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.markdown-content :deep(ul li) {
  list-style-type: disc;
}

.markdown-content :deep(ol li) {
  list-style-type: decimal;
}

.markdown-content :deep(ul ul),
.markdown-content :deep(ol ol) {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

/* 引用样式 */
.markdown-content :deep(blockquote) {
  background: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 15px 20px;
  margin: 1.5rem 0;
  font-style: italic;
  color: #555;
  border-radius: 0 4px 4px 0;
}

.markdown-content :deep(blockquote p) {
  margin-bottom: 0;
}

.markdown-content :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

/* 代码样式 */
.markdown-content :deep(code) {
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  color: #e74c3c;
}

.markdown-content :deep(pre) {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid #e9ecef;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  color: #333;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* 链接样式 */
.markdown-content :deep(a) {
  color: #007bff;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.markdown-content :deep(a:hover) {
  color: #0056b3;
  border-bottom-color: #0056b3;
}

/* 表格样式 */
.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: white;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.markdown-content :deep(th) {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

.markdown-content :deep(tr:hover) {
  background: #f8f9fa;
}

/* 水平分割线 */
.markdown-content :deep(hr) {
  border: none;
  height: 1px;
  background: #e9ecef;
  margin: 2rem 0;
}

/* 图片样式 */
.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
  margin: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 暗色模式支持 */
body.dark-mode .markdown-content {
  color: var(--text-primary);
}

body.dark-mode .markdown-content :deep(h1),
body.dark-mode .markdown-content :deep(h2),
body.dark-mode .markdown-content :deep(h3),
body.dark-mode .markdown-content :deep(h4),
body.dark-mode .markdown-content :deep(h5),
body.dark-mode .markdown-content :deep(h6) {
  color: var(--text-primary);
}

body.dark-mode .markdown-content :deep(strong) {
  color: var(--text-accent);
}

body.dark-mode .markdown-content :deep(em) {
  color: var(--text-secondary);
}

body.dark-mode .markdown-content :deep(blockquote) {
  background: #2d2d2d;
  color: #c0c0c0;
  border-left-color: #007bff;
}

body.dark-mode .markdown-content :deep(code) {
  background: #404040;
  color: #ff6b6b;
}

body.dark-mode .markdown-content :deep(pre) {
  background: #2d2d2d;
  border-color: #404040;
}

body.dark-mode .markdown-content :deep(pre code) {
  color: #e0e0e0;
}

body.dark-mode .markdown-content :deep(a) {
  color: #4dabf7;
}

body.dark-mode .markdown-content :deep(a:hover) {
  color: #74c0fc;
}

body.dark-mode .markdown-content :deep(table) {
  background: #2d2d2d;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

body.dark-mode .markdown-content :deep(th) {
  background: #404040;
  color: #e0e0e0;
}

body.dark-mode .markdown-content :deep(td) {
  border-bottom-color: #404040;
}

body.dark-mode .markdown-content :deep(tr:hover) {
  background: #404040;
}

body.dark-mode .markdown-content :deep(hr) {
  background: #404040;
}

body.dark-mode .markdown-content :deep(img) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
</style>
