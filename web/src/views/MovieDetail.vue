<template>
  <div class="movie-detail">
    <!-- 标题和编辑按钮 -->
    <div class="title-container">
      <h1>{{ movie.title }}</h1>
      <div class="edit-buttons">
        <el-tooltip content="编辑影片信息" placement="top">
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
    <img :src="movie.cover" alt="封面" class="cover" @error="setDefaultCover($event)" />
    <p>
      <strong>主演：</strong>
      <span v-if="movie.actors">
        <el-tag
          v-for="(actor, index) in movie.actors.split(', ')"
          :key="index"
          :type="getActorTagType(actor.trim())"
          class="actor-tag"
          @click="goToActor(actor.trim())"
        >
          {{ actor }}
        </el-tag>
      </span>
      <span v-else>暂无演员信息</span>
    </p>
    <!-- 评分 -->
    <div class="rating">
      <strong>评分：</strong>
      <span v-for="i in 5" :key="i" class="star">
        <span class="material-icons" :class="{ filled: i <= movie.rating }">
          {{ i <= movie.rating ? 'star' : 'star_border' }}
        </span>
      </span>
    </div>
    <p>
      <strong>标签：</strong>
      <span v-if="movie.tags">
        <el-tag
          v-for="(tag, index) in movie.tags"
          :key="index"
          :type="getTagType(tag.trim())"
          effect="plain"
          class="tag-item"
          @click="goToTagDetail(tag.trim())"
        >
          {{ tag }}
        </el-tag>
      </span>
      <span v-else>暂无标签信息</span>
    </p>
    <p><strong>简介：</strong>{{ movie.description }}</p>

    <!-- 显示 Markdown 正文 -->
    <div class="content" v-if="!editBodyDialogVisible">
      <MarkdownRender :content="movie.body" />
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
        v-model="movie.body"
        :title="`编辑《${movie.title}》正文`"
        :movie-id="movie.id"
        @saved="onBodySaved"
        @cancelled="editBodyDialogVisible = false"
      />
    </el-dialog>

    <!-- 上一页、下一页按钮 -->
    <div class="navigation">
      <button @click="navigate(-1)" :disabled="!prevMovie">上一页</button>
      <button @click="goBack">返回</button>
      <button @click="navigate(1)" :disabled="!nextMovie">下一页</button>
    </div>

    <!-- 编辑元信息对话框 -->
    <MetaEditor
      v-model:visible="editDialogVisible"
      type="movie"
      :data="movie"
      :id="movie.id"
      @saved="onMetaSaved"
      @cancelled="editDialogVisible = false"
    />
  </div>
</template>

<script>
import axios from 'axios'
import { Setting, Document } from '@element-plus/icons-vue'
import LiveEditor from '@/components/LiveEditor.vue'
import MetaEditor from '@/components/MetaEditor.vue'
import MarkdownRender from '@/components/MarkdownRender.vue'

export default {
  name: 'MovieDetail',
  components: {
    Setting,
    Document,
    LiveEditor,
    MetaEditor,
    MarkdownRender,
  },
  data() {
    return {
      movie: {},
      prevMovie: null,
      nextMovie: null,
      editDialogVisible: false, // 控制编辑对话框的显示状态
      editBodyDialogVisible: false, // 控制编辑正文对话框的显示状态
    }
  },

  async created() {
    const { id } = this.$route.params
    const allMovies = await this.fetchMovies()
    const currentIndex = allMovies.findIndex((m) => m.id === id)

    if (currentIndex !== -1) {
      this.movie = allMovies[currentIndex]
      this.prevMovie = currentIndex > 0 ? allMovies[currentIndex - 1] : null
      this.nextMovie = currentIndex < allMovies.length - 1 ? allMovies[currentIndex + 1] : null
    }

    // 监听影片创建事件，因为可能会影响相邻影片
    this.$eventBus.on('movie-created', () => {
      this.refreshMovieData()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('movie-created')
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get('/api/movies') // 调用后端 API [[2]]
        return response.data // 返回电影列表
      } catch (error) {
        console.error('请求失败:', error)
      }
    },
    openEditMetaDialog() {
      this.editDialogVisible = true // 打开编辑对话框
    },
    openEditBodyDialog() {
      this.editBodyDialogVisible = true // 打开编辑正文对话框
    },
    onMetaSaved() {
      // 刷新整个页面以显示更新后的信息
      location.reload()
    },

    async onBodySaved(newBody) {
      // 更新本地数据
      this.movie.body = newBody
      this.editBodyDialogVisible = false
    },
    setDefaultCover(event) {
      event.target.src = '/imgs/default_cover.jpg' // 默认图片路径
    },
    navigate(direction) {
      const targetMovie = direction === -1 ? this.prevMovie : this.nextMovie
      if (targetMovie) {
        this.$router.push({
          name: 'MovieDetail',
          params: { id: targetMovie.id },
        })
      }
    },
    goBack() {
      this.$router.go(-1) // 返回上一页 [[7]]
    },
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
    },
    goToActor(name) {
      console.log('跳转到演员详情页，演员姓名:', name) // 调试信息
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
    },
    goToTagDetail(tagName) {
      this.$router.push(`/tags/${tagName}`) // 跳转到标签详情页面
    },
    getActorTagType(actorName) {
      // 根据演员名字生成固定的类型映射 [[6]]
      const types = ['success', 'info', 'warning', 'danger']
      const typeIndex = Math.abs(this.hashCode(actorName)) % types.length
      return types[typeIndex]
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
    async refreshMovieData() {
      const { id } = this.$route.params
      const allMovies = await this.fetchMovies()
      const currentIndex = allMovies.findIndex((m) => m.id === id)

      if (currentIndex !== -1) {
        this.movie = allMovies[currentIndex]
        this.prevMovie = currentIndex > 0 ? allMovies[currentIndex - 1] : null
        this.nextMovie = currentIndex < allMovies.length - 1 ? allMovies[currentIndex + 1] : null
      }
    },
  },
}
</script>

<style scoped>
.logo img {
  width: 100px;
  cursor: pointer;
}

/* title-container 样式已移至 article-title.scss */

.movie-detail {
  padding: 20px;
  max-width: 800px;
  margin: auto;
  background: var(--bg-gradient-light);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
}

.movie-detail h1 {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 20px;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.movie-detail p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 15px;
}

.movie-detail strong {
  color: var(--primary-color);
  font-weight: 600;
}

.actor-tag {
  margin-right: 8px;
  margin-bottom: 5px;
  cursor: pointer;
  border: 1px solid var(--border-medium);
  transition: all 0.3s ease;
}

.actor-tag:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.tag-item {
  margin-right: 8px;
  margin-bottom: 5px;
  border: 1px solid var(--border-medium);
  transition: all 0.3s ease;
}

.tag-item:hover {
  cursor: pointer;
  background: var(--bg-gradient-medium);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.cover {
  max-width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  margin-top: 20px;
  border-radius: 12px;
  border: 2px solid var(--border-light);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
}

.cover:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.navigation {
  margin-top: 30px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

button {
  padding: 12px 24px;
  cursor: pointer;
  position: relative;
  background: var(--btn-primary-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
}

button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
  box-shadow: none;
}

button:disabled:hover {
  transform: none;
}

.content {
  margin-top: 30px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--card-border);
  box-shadow: var(--shadow-sm);
}

.rating {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 15px;
}

.star {
  font-size: 24px;
  color: #ddd;
  transition: all 0.2s ease;
}

.star .material-icons.filled {
  color: #ffca28;
  text-shadow: 0 2px 4px rgba(255, 202, 40, 0.3);
}

/* 编辑按钮样式已移至 article-title.scss */

/* 响应式设计已移至 article-title.scss */

/* 编辑正文对话框样式 */
:deep(.body-editor-dialog .el-dialog) {
  height: 90vh;
}

:deep(.body-editor-dialog .el-dialog__body) {
  height: calc(90vh - 120px);
  padding: 0;
}

</style>
