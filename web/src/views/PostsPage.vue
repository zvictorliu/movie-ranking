<template>
  <div class="posts-container">
    <div class="posts-header">
      <h1>博客文章</h1>
      <p>分享电影评论、推荐和思考</p>
    </div>

    <!-- 筛选器 -->
    <div class="filter-container">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文章标题或内容..."
          clearable
          @input="filterPosts"
        >
          <template #prefix>
            <el-icon><SearchIcon /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="tag-filter">
        <el-select
          v-model="selectedTags"
          multiple
          clearable
          filterable
          placeholder="按标签筛选"
          style="width: 200px"
          @change="filterPosts"
        >
          <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="posts-list">
      <div
        v-for="post in filteredPosts"
        :key="post.slug"
        class="post-card"
        @click="goToPost(post.slug)"
      >
        <div class="post-header">
          <h2 class="post-title">{{ post.title }}</h2>
          <div class="post-meta">
            <span class="post-date">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(post.date) }}
            </span>
            <span class="post-author">
              <el-icon><User /></el-icon>
              {{ post.author }}
            </span>
          </div>
        </div>

        <div class="post-excerpt">
          {{ post.excerpt }}
        </div>

        <div class="post-tags">
          <el-tag
            v-for="tag in post.tags"
            :key="tag"
            :type="getTagType(tag)"
            effect="plain"
            size="small"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </div>

        <div class="post-footer">
          <el-button type="primary" size="small" @click.stop="goToPost(post.slug)">
            阅读全文
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredPosts.length === 0" class="empty-state">
      <el-empty description="暂无符合条件的文章" />
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredPosts.length"
        layout="prev, pager, next, jumper"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import { Calendar, User, ArrowRight, Search as SearchIcon } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'PostsPage',
  components: {
    Calendar,
    User,
    SearchIcon,
    ArrowRight,
  },
  data() {
    return {
      posts: [],
      filteredPosts: [],
      searchQuery: '',
      selectedTags: [],
      allTags: [],
      currentPage: 1,
      pageSize: 6,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredPosts.length / this.pageSize)
    },
    paginatedPosts() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredPosts.slice(start, end)
    },
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get('/api/posts')
        this.posts = response.data.posts || []
        this.filteredPosts = [...this.posts]
        this.extractAllTags()
      } catch (error) {
        console.error('获取文章列表失败:', error)
        // 如果API不可用，使用本地数据
        this.loadLocalPosts()
      }
    },
    loadLocalPosts() {
      // 模拟本地文章数据
      this.posts = [
        {
          slug: 'hello-world',
          title: 'Hello World - 我的第一篇博客',
          date: '2024-01-15',
          author: '电影爱好者',
          tags: ['介绍', '电影', '博客'],
          excerpt: '欢迎来到我的电影博客！这里将分享我对各种电影的看法和评论。',
        },
        {
          slug: 'movie-review-2024',
          title: '2024年最值得期待的电影',
          date: '2024-01-20',
          author: '电影评论家',
          tags: ['2024', '新片', '期待', '好莱坞'],
          excerpt: '2024年即将上映的精彩电影盘点，从科幻大片到文艺佳作，总有一部适合你。',
        },
        {
          slug: 'classic-movies-recommendation',
          title: '经典电影推荐：那些值得反复观看的佳作',
          date: '2024-01-25',
          author: '资深影迷',
          tags: ['经典', '推荐', '回顾', '必看'],
          excerpt: '精选十部经典电影，每一部都是电影史上的瑰宝，值得每个电影爱好者收藏和反复观看。',
        },
      ]
      this.filteredPosts = [...this.posts]
      this.extractAllTags()
    },
    extractAllTags() {
      const tagsSet = new Set()
      this.posts.forEach((post) => {
        if (post.tags && Array.isArray(post.tags)) {
          post.tags.forEach((tag) => tagsSet.add(tag))
        }
      })
      this.allTags = Array.from(tagsSet).sort()
    },
    filterPosts() {
      let filtered = [...this.posts]

      // 按搜索关键词筛选
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          (post) =>
            post.title.toLowerCase().includes(query) ||
            post.excerpt.toLowerCase().includes(query) ||
            post.author.toLowerCase().includes(query),
        )
      }

      // 按标签筛选
      if (this.selectedTags.length > 0) {
        filtered = filtered.filter(
          (post) => post.tags && this.selectedTags.some((tag) => post.tags.includes(tag)),
        )
      }

      this.filteredPosts = filtered
      this.currentPage = 1 // 重置到第一页
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
    handlePageChange(page) {
      this.currentPage = page
    },
  },
  mounted() {
    this.fetchPosts()

    // 监听博客创建事件
    this.$eventBus.on('post-created', () => {
      this.fetchPosts()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('post-created')
  },
}
</script>

<style scoped>
.posts-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.posts-header {
  text-align: center;
  margin-bottom: 40px;
}

.posts-header h1 {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 10px;
  font-weight: 600;
  text-shadow: var(--shadow-sm);
}

.posts-header p {
  font-size: 1.1rem;
  color: var(--secondary-color);
  font-weight: 500;
}

.filter-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  align-items: center;
  flex-wrap: wrap;
  padding: 20px;
  background: var(--bg-gradient-light);
  border-radius: 12px;
  border: 2px solid var(--border-light);
}

.search-box {
  flex: 1;
  min-width: 300px;
}

.tag-filter {
  min-width: 200px;
}

.posts-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.post-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 25px;
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid var(--card-border);
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.post-header {
  margin-bottom: 15px;
}

.post-title {
  font-size: 1.4rem;
  color: var(--primary-color);
  margin-bottom: 10px;
  line-height: 1.4;
  font-weight: 600;
}

.post-meta {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: var(--secondary-color);
  align-items: center;
}

.post-date,
.post-author {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-excerpt {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.tag-item {
  font-size: 0.8rem;
}

.post-footer {
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .posts-container {
    padding: 15px;
  }

  .posts-header h1 {
    font-size: 2rem;
  }

  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: auto;
  }

  .posts-list {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .post-card {
    padding: 20px;
  }

  .post-meta {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}

</style>
