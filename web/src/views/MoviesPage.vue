<template>
  <div class="movies-container">
    <!-- 影片视图 -->
    <div class="movie-view">
      <div class="save-button-container">
        <button
          @click="saveRanking"
          class="save-button"
          :class="{ saving: savingRanking }"
          :disabled="savingRanking"
          :title="savingRanking ? '保存中...' : '保存排行'"
        >
          <span class="material-icons">{{ savingRanking ? 'hourglass_empty' : 'save' }}</span>
          <span class="button-text">{{ savingRanking ? '保存中...' : '保存排行' }}</span>
        </button>
      </div>
      <!-- 筛选器 -->
      <div class="filter-container">
        <!-- 搜索框 -->
        <div class="search-filter">
          <label for="search-input">搜索：</label>
          <el-input
            v-model="searchQuery"
            placeholder="搜索影片标题、演员或标签..."
            clearable
            style="width: 300px"
            @input="filterMovies"
            @clear="filterMovies"
          >
            <template #prefix>
              <el-icon><SearchIcon /></el-icon>
            </template>
          </el-input>
        </div>

        <div class="filter-row">
          <div class="actor-filter">
            <label for="actor-filter">按演员筛选：</label>
            <el-select
              v-model="selectedActors"
              multiple
              clearable
              filterable
              placeholder="请选择演员"
              style="width: 150px"
              @change="filterMovies"
            >
              <el-option
                v-for="actor in actors"
                :key="actor.name"
                :label="actor.name"
                :value="actor.name"
              ></el-option>
            </el-select>
          </div>

          <div class="tag-filter">
            <label for="tag-filter">按标签筛选：</label>
            <el-select
              v-model="selectedTags"
              multiple
              clearable
              filterable
              placeholder="请选择标签"
              style="width: 150px"
              @change="filterMovies"
            >
              <el-option
                v-for="tag in availableTags"
                :key="tag"
                :label="tag"
                :value="tag"
              ></el-option>
            </el-select>
          </div>

          <div class="rating-filter">
            <label for="rating-filter">按评分筛选：</label>
            <el-slider
              v-model="ratingRange"
              range
              :min="0"
              :max="5"
              :step="1"
              style="width: 100px"
              @change="filterMovies"
            ></el-slider>
            <span style="margin-left: 20px">{{ ratingRange[0] }} - {{ ratingRange[1] }}</span>
          </div>
        </div>

        <!-- 清除筛选器按钮 -->
        <div class="filter-actions">
          <el-button size="small" @click="clearAllFilters" :disabled="!hasActiveFilters">
            清除所有筛选
          </el-button>
          <span class="filter-count" v-if="hasActiveFilters">
            已筛选 {{ filteredMovies.length }} 部影片
          </span>
        </div>
      </div>

      <MoviePreview
        v-for="(movie, index) in filteredMovies"
        :key="movie.id"
        :title="movie.title"
        :allow-rating="true"
      >
        <template #controls>
          <!-- 上移/下移按钮 -->
          <div class="controls">
            <button @click="moveUp(index)" :disabled="index === 0" class="up-down-button">
              <el-icon><ArrowUp /></el-icon>
            </button>
            <button @click="openEditDialog(movie)" class="edit-movie-button">
              <el-icon><EditPen /></el-icon>
            </button>
            <button
              @click="moveDown(index)"
              :disabled="index === movies.length - 1"
              class="up-down-button"
            >
              <el-icon><ArrowDown /></el-icon>
            </button>
          </div>
        </template>
      </MoviePreview>
    </div>

    <!-- 编辑元信息对话框 -->
    <MetaEditor
      v-model:visible="editDialogVisible"
      type="movie"
      :data="editFormData"
      :id="editFormData.id"
      @saved="onMetaSaved"
      @cancelled="editDialogVisible = false"
    />
  </div>
</template>

<script>
// 导入 Element Plus 图标
import { ArrowUp, ArrowDown, EditPen, Search } from '@element-plus/icons-vue'

import axios from 'axios'
import { useViewStore } from '../store/view'
import MetaEditor from '@/components/MetaEditor.vue'
import MoviePreview from '@/components/MoviePreview.vue'

export default {
  name: 'MoviesPage',
  components: {
    ArrowUp,
    ArrowDown,
    EditPen,
    SearchIcon: Search,
    MetaEditor,
    MoviePreview,
  },
  setup() {
    const viewStore = useViewStore()
    return { viewStore }
  },
  data() {
    return {
      movies: [], // 初始为空数组，稍后加载数据
      actors: [], // 演员列表
      filteredMovies: [], // 筛选后的影片
      selectedActors: [], // 当前选择的演员
      selectedTags: [], // 当前选择的标签
      searchQuery: '', // 搜索查询
      ratingRange: [3, 5], // 默认评分区间
      defaultCover: '/imgs/default_cover.jpg', // 默认封面图片路径
      editDialogVisible: false, // 控制编辑对话框的显示状态
      editFormData: {}, // 当前正在编辑的影片数据
      savingRanking: false, // 保存排行的状态
    }
  },
  computed: {
    // 获取所有可用的标签
    availableTags() {
      const allTags = new Set()
      this.movies.forEach((movie) => {
        if (movie.tags && Array.isArray(movie.tags)) {
          movie.tags.forEach((tag) => allTags.add(tag.trim()))
        }
      })
      return Array.from(allTags).sort()
    },
    // 检查是否有活跃的筛选器
    hasActiveFilters() {
      return (
        this.searchQuery.trim() ||
        this.selectedActors.length > 0 ||
        this.selectedTags.length > 0 ||
        this.ratingRange[0] !== 3 ||
        this.ratingRange[1] !== 5
      )
    },
  },
  methods: {
    moveUp(index) {
      if (this.filteredMovies.length !== this.movies.length) {
        this.$message.warning('请显示全部影片后再排序')
        return
      }
      if (index > 0) {
        const temp = this.filteredMovies[index]
        this.filteredMovies.splice(index, 1)
        this.filteredMovies.splice(index - 1, 0, temp)

        // 滚动到目标影片
        this.scrollToMovie(index - 1)
      }
    },
    moveDown(index) {
      if (this.filteredMovies.length !== this.movies.length) {
        this.$message.warning('请显示全部影片后再排序')
        return
      }
      if (index < this.filteredMovies.length - 1) {
        const temp = this.filteredMovies[index]
        this.filteredMovies.splice(index, 1)
        this.filteredMovies.splice(index + 1, 0, temp)

        // 滚动到目标影片
        this.scrollToMovie(index + 1)
      }
    },
    scrollToMovie(index) {
      // 获取目标影片的 DOM 元素
      this.$nextTick(() => {
        const movieElement = this.$el.querySelectorAll('.movie-item')[index]
        if (movieElement) {
          movieElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },
    // 以下方法已移至 MoviePreview 组件：goToDetail, goToActor, goToTagDetail, getActorTagType, getTagType, hashCode
    filterMovies() {
      let filtered = [...this.movies]

      // 1. 搜索筛选（标题、演员、标签）
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim()
        filtered = filtered.filter((movie) => {
          // 搜索标题
          if (movie.title && movie.title.toLowerCase().includes(query)) {
            return true
          }
          // 搜索演员
          if (movie.actors && movie.actors.toLowerCase().includes(query)) {
            return true
          }
          // 搜索标签
          if (movie.tags && Array.isArray(movie.tags)) {
            return movie.tags.some((tag) => tag.toLowerCase().includes(query))
          }
          return false
        })
      }

      // 2. 演员筛选
      if (this.selectedActors.length > 0) {
        filtered = filtered.filter((movie) =>
          this.selectedActors.some(
            (actor) => movie.actors && movie.actors.split(', ').includes(actor),
          ),
        )
      }

      // 3. 标签筛选
      if (this.selectedTags.length > 0) {
        filtered = filtered.filter((movie) =>
          this.selectedTags.some(
            (selectedTag) =>
              movie.tags &&
              Array.isArray(movie.tags) &&
              movie.tags.some((tag) => tag.trim() === selectedTag),
          ),
        )
      }

      // 4. 评分区间筛选
      if (this.ratingRange[0] >= 0 || this.ratingRange[1] <= 5) {
        filtered = filtered.filter(
          (movie) => movie.rating >= this.ratingRange[0] && movie.rating <= this.ratingRange[1],
        )
      }

      this.filteredMovies = filtered
    },
    // 清除所有筛选器
    clearAllFilters() {
      this.searchQuery = ''
      this.selectedActors = []
      this.selectedTags = []
      this.ratingRange = [3, 5]
      this.filterMovies()
    },
    openEditDialog(movie) {
      this.editFormData = { ...movie } // 复制当前影片的数据
      this.editDialogVisible = true // 打开编辑对话框
    },
    onMetaSaved() {
      // 更新本地影片数据
      this.fetchMovies()
      this.filterMovies()
    },

    async saveRanking() {
      if (this.savingRanking) return // 防止重复点击

      this.savingRanking = true
      const newRanking = this.filteredMovies.map((movie, index) => ({
        id: movie.id,
        order: index + 1, // 更新顺序值
        rating: movie.rating || 0, // 如果没有评分，默认为 0
      }))
      try {
        await axios.post('/api/update-ranking', { ranking: newRanking })

        // 添加成功动画效果
        const saveButton = this.$el.querySelector('.save-button')
        if (saveButton) {
          saveButton.classList.add('success')
          setTimeout(() => {
            saveButton.classList.remove('success')
          }, 2000)
        }

        this.$message.success('排行已更新！')
        this.fetchMovies() // 重新获取影片列表
      } catch (error) {
        console.error('Error updating ranking:', error)
        this.$message.error('更新失败，请稍后再试！')
      } finally {
        this.savingRanking = false
      }
    },
    async fetchMovies() {
      try {
        const response = await axios.get('/api/movies') // 调用后端 API [[2]]
        this.movies = response.data
        this.filteredMovies = response.data // 初始化筛选后的影片
        this.filterMovies() // 初始化筛选
      } catch (error) {
        console.error('请求失败:', error)
      }
    },
    async fetchActors() {
      try {
        const response = await axios.get('/api/actors')
        this.actors = response.data
      } catch (error) {
        console.error('Error fetching actors:', error)
      }
    },
  },
  async created() {
    try {
      await this.fetchMovies() // 获取影片列表
      await this.fetchActors() // 获取演员列表
    } catch (error) {
      console.error('Error:', error)
    }
  },
}
</script>

<style scoped>
.movies-container {
  font-family: Arial, sans-serif;
  align-items: center;
}

.movie-view {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.save-button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

/* 电影项样式已移至 MoviePreview 组件，这里只保留控制按钮样式 */

.controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 10px;
}

@media (max-width: 768px) {
  .controls {
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
}

.edit-movie-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #409eff;
}

.up-down-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #409eff;
}

.up-down-button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.save-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #42b983 0%, #3aa876 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(66, 185, 131, 0.3);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
}

.save-button::before {
  content: attr(title);
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  pointer-events: none;
}

.save-button:hover::before {
  opacity: 1;
  visibility: visible;
}

.save-button:hover {
  background: linear-gradient(135deg, #3aa876 0%, #2d8f5f 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(66, 185, 131, 0.4);
}

.save-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(66, 185, 131, 0.3);
}

.save-button .material-icons {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.save-button:hover .material-icons {
  transform: rotate(360deg);
}

.save-button.saving {
  background: linear-gradient(135deg, #718096 0%, #4a5568 100%);
  cursor: not-allowed;
  pointer-events: none;
}

.save-button.saving .material-icons {
  animation: spin 1s linear infinite;
}

.save-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.save-button.success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  animation: successPulse 0.6s ease-in-out;
}

@keyframes successPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.filter-container {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.search-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-filter label {
  font-weight: 500;
  color: #333;
  min-width: 60px;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.actor-filter,
.tag-filter,
.rating-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.actor-filter label,
.tag-filter label,
.rating-filter label {
  font-weight: 500;
  color: #333;
  min-width: 80px;
}

.rating-filter span {
  margin-left: 10px;
  font-weight: 500;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .search-filter {
    width: 100%;
  }

  .search-filter .el-input {
    width: 100% !important;
  }
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
}

.filter-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .save-button {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    box-shadow: 0 4px 15px rgba(45, 55, 72, 0.3);
  }

  .save-button:hover {
    background: linear-gradient(135deg, #1a202c 0%, #0f1419 100%);
    box-shadow: 0 6px 20px rgba(45, 55, 72, 0.4);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .save-button {
    padding: 10px 16px;
    font-size: 14px;
  }

  .save-button .material-icons {
    font-size: 16px;
  }
}
</style>
