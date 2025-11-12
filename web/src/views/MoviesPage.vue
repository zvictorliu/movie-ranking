<template>
  <div class="movies-container">
    <!-- 影片视图 -->
    <div class="movie-view">
      <!-- 顶部操作栏 -->
      <div class="top-bar">
        <div class="page-title">
          <h1>电影排行管理</h1>
          <p class="subtitle">管理您的电影收藏和排行</p>
        </div>

        <div class="top-actions">
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
      </div>

      <!-- 幻灯片模块 -->
      <div class="slideshow-section" v-if="slideshowMovies.length">
        <div
          class="slideshow-track"
          :style="slideshowTrackStyle"
          @touchstart.passive="onSlideshowTouchStart"
          @touchmove.passive="onSlideshowTouchMove"
          @touchend="onSlideshowTouchEnd"
          @touchcancel="onSlideshowTouchEnd"
        >
          <div
            v-for="(movie, index) in slideshowMovies"
            :key="movie.id || `slide-${index}`"
            class="slideshow-slide"
            :class="{ active: index === currentSlideIndex }"
            :style="{ backgroundImage: `url(${movie.cover || defaultCover})` }"
            role="button"
            tabindex="0"
            :aria-label="movie.title ? `查看${movie.title}详情` : '查看影片详情'"
            @click="goToMovieDetail(movie)"
            @keyup.enter.prevent="goToMovieDetail(movie)"
          >
            <div class="slide-info">
              <h3>{{ movie.title }}</h3>
              <p>{{ movie.description || '暂无简介' }}</p>
              <div class="slide-meta">
                <span>
                  评分：{{
                    movie.rating !== undefined && movie.rating !== null ? movie.rating : '暂无'
                  }}
                </span>
                <span v-if="movie.actors">主演：{{ movie.actors }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="slideshow-dots" v-if="slideshowMovies.length > 1">
          <button
            v-for="(movie, index) in slideshowMovies"
            :key="`slide-dot-${movie.id || index}`"
            class="slideshow-dot"
            :class="{ active: index === currentSlideIndex }"
            @click="goToSlide(index)"
            type="button"
            aria-label="切换幻灯片"
          ></button>
        </div>
      </div>

      <!-- 筛选器面板 -->
      <div class="filter-panel">
        <div class="filter-header">
          <h3>筛选与搜索</h3>
          <el-button
            size="small"
            type="info"
            plain
            @click="clearAllFilters"
            :disabled="!hasActiveFilters"
          >
            <el-icon><DeleteIcon /></el-icon>
            清除筛选
          </el-button>
        </div>

        <!-- 搜索区域 -->
        <div class="search-section">
          <el-input
            v-model="searchQuery"
            placeholder="搜索影片标题、演员或标签..."
            clearable
            size="large"
            @input="filterMovies"
            @clear="filterMovies"
          >
            <template #prefix>
              <el-icon><SearchIcon /></el-icon>
            </template>
          </el-input>
        </div>

        <!-- 筛选器区域 -->
        <div class="filters-section">
          <div class="filter-group">
            <label class="filter-label">演员筛选</label>
            <el-select
              v-model="selectedActors"
              multiple
              clearable
              filterable
              placeholder="选择演员"
              style="width: 200px"
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

          <div class="filter-group">
            <label class="filter-label">标签筛选</label>
            <el-select
              v-model="selectedTags"
              multiple
              clearable
              filterable
              placeholder="选择标签"
              style="width: 200px"
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

          <div class="filter-group">
            <label class="filter-label">评分范围</label>
            <div class="rating-slider-container">
              <el-slider
                v-model="ratingRange"
                range
                :min="0"
                :max="5"
                :step="1"
                style="width: 150px"
                @change="filterMovies"
              ></el-slider>
              <span class="rating-display">{{ ratingRange[0] }} - {{ ratingRange[1] }}</span>
            </div>
          </div>
        </div>

        <!-- 筛选结果统计 -->
        <div class="filter-stats" v-if="hasActiveFilters">
          <el-tag type="info" size="large">
            <el-icon><FilterIcon /></el-icon>
            已筛选 {{ filteredMovies.length }} 部影片
          </el-tag>
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
import { ArrowUp, ArrowDown, EditPen, Search, Delete, Filter } from '@element-plus/icons-vue'

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
    DeleteIcon: Delete,
    FilterIcon: Filter,
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
      minRatingThreshold: 3, // 评分最低限制
      defaultCover: '/imgs/default_cover.jpg', // 默认封面图片路径
      editDialogVisible: false, // 控制编辑对话框的显示状态
      editFormData: {}, // 当前正在编辑的影片数据
      savingRanking: false, // 保存排行的状态
      slideshowMovies: [], // 用于幻灯片展示的影片
      currentSlideIndex: 0, // 当前幻灯片索引
      slideshowTimer: null, // 幻灯片自动播放计时器
      touchStartX: null, // 触摸起点 X
      touchDeltaX: 0, // 触摸移动距离
      ignoreNextSlideClick: false, // 是否忽略下一次点击（防止滑动触发）
      dragOffsetX: 0, // 拖拽时的位移偏移
      isDragging: false, // 当前是否正在拖拽
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
    slideshowTrackStyle() {
      const basePercent = this.currentSlideIndex * 100
      const offsetPx = this.dragOffsetX || 0
      return {
        transform: `translateX(calc(-${basePercent}% + ${offsetPx}px))`,
        transition: this.isDragging ? 'none' : 'transform 0.6s ease',
        willChange: 'transform',
      }
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
    refreshSlideshow() {
      this.updateSlideshowMovies()
      this.startSlideshow()
    },
    updateSlideshowMovies() {
      if (!this.movies.length) {
        this.slideshowMovies = []
        this.currentSlideIndex = 0
        this.stopSlideshow()
        this.resetDragState()
        return
      }
      const eligibleMovies = this.movies.filter((movie) => {
        const rating = Number(movie.rating)
        return !Number.isNaN(rating) && rating >= this.minRatingThreshold
      })
      if (!eligibleMovies.length) {
        this.slideshowMovies = []
        this.currentSlideIndex = 0
        this.stopSlideshow()
        this.resetDragState()
        return
      }
      const shuffled = [...eligibleMovies]
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
      }
      this.slideshowMovies = shuffled.slice(0, Math.min(10, shuffled.length))
      this.currentSlideIndex = 0
      this.resetDragState()
    },
    startSlideshow() {
      this.stopSlideshow()
      if (this.slideshowMovies.length <= 1) {
        return
      }
      this.slideshowTimer = setInterval(() => {
        this.nextSlide()
      }, 10000)
    },
    stopSlideshow() {
      if (this.slideshowTimer) {
        clearInterval(this.slideshowTimer)
        this.slideshowTimer = null
      }
    },
    nextSlide() {
      if (!this.slideshowMovies.length) {
        return
      }
      this.currentSlideIndex = (this.currentSlideIndex + 1) % this.slideshowMovies.length
      this.resetDragState()
    },
    prevSlide() {
      if (!this.slideshowMovies.length) {
        return
      }
      const total = this.slideshowMovies.length
      this.currentSlideIndex = (this.currentSlideIndex - 1 + total) % total
      this.resetDragState()
    },
    goToSlide(index) {
      if (index < 0 || index >= this.slideshowMovies.length) {
        return
      }
      this.currentSlideIndex = index
      this.resetDragState()
      this.startSlideshow()
    },
    goToMovieDetail(movie) {
      if (this.ignoreNextSlideClick) {
        this.ignoreNextSlideClick = false
        return
      }
      if (!movie || !movie.id) {
        return
      }
      this.$router.push({ name: 'MovieDetail', params: { id: movie.id } })
    },
    onSlideshowTouchStart(event) {
      if (!event.touches || event.touches.length !== 1) {
        return
      }
      this.touchStartX = event.touches[0].clientX
      this.touchDeltaX = 0
      this.ignoreNextSlideClick = false
      this.dragOffsetX = 0
      this.isDragging = true
      this.stopSlideshow()
    },
    onSlideshowTouchMove(event) {
      if (this.touchStartX === null || !event.touches || event.touches.length !== 1) {
        return
      }
      this.touchDeltaX = event.touches[0].clientX - this.touchStartX
      this.dragOffsetX = this.touchDeltaX
    },
    onSlideshowTouchEnd() {
      if (this.touchStartX === null) {
        return
      }
      const swipeThreshold = 50
      const isSwipe = Math.abs(this.touchDeltaX) > swipeThreshold
      if (isSwipe) {
        if (this.touchDeltaX > 0) {
          this.prevSlide()
        } else {
          this.nextSlide()
        }
      }
      this.ignoreNextSlideClick = isSwipe
      if (isSwipe) {
        setTimeout(() => {
          this.ignoreNextSlideClick = false
        }, 120)
      }
      this.touchStartX = null
      this.touchDeltaX = 0
      this.resetDragState()
      this.startSlideshow()
    },
    resetDragState() {
      this.dragOffsetX = 0
      this.isDragging = false
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
        this.refreshSlideshow()
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

    // 监听影片创建事件
    this.$eventBus.on('movie-created', () => {
      this.fetchMovies()
      this.fetchActors()
    })

    // 监听演员创建事件
    this.$eventBus.on('actor-created', () => {
      this.fetchActors()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.stopSlideshow()
    this.$eventBus.off('movie-created')
    this.$eventBus.off('actor-created')
  },
}
</script>

<style scoped>
.movies-container {
  font-family: Arial, sans-serif;
  align-items: center;
}

.movie-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 5px;
}

.slideshow-section {
  position: relative;
  margin: 20px 0 40px;
  border-radius: 18px;
  overflow: hidden;
  background: #000;
  aspect-ratio: 16 / 9;
  width: 100%;
  max-width: 100%;
  box-shadow: var(--shadow-lg);
}

.slideshow-track {
  position: relative;
  display: flex;
  width: 100%;
  height: 100%;
  touch-action: pan-y;
  will-change: transform;
}

.slideshow-slide {
  position: relative;
  flex: 0 0 100%;
  height: 100%;
  aspect-ratio: 16 / 9;
  background-size: cover;
  background-position: center;
  cursor: pointer;
  overflow: hidden;
}

.slideshow-slide::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.35));
}

.slideshow-slide:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.slide-info {
  position: absolute;
  bottom: 72px;
  left: 24px;
  right: 24px;
  color: #fff;
  z-index: 2;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}

.slide-info h3 {
  margin: 0 0 12px;
  font-size: 26px;
  font-weight: 600;
}

.slide-info p {
  margin: 0 0 12px;
  line-height: 1.5;
  max-width: 720px;
  font-size: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.slide-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 14px;
  opacity: 0.9;
}

.slideshow-dots {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 3;
}

.slideshow-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: width 0.3s ease, background 0.3s ease;
}

.slideshow-dot.active {
  width: 32px;
  background: #fff;
}

@media (max-width: 768px) {
  .slideshow-section {
    width: 100%;
    max-width: 100%;
  }

  .slideshow-track {
    height: 100%;
  }

  .slide-info {
    left: 16px;
    right: 16px;
    bottom: 44px;
  }

  .slide-info h3 {
    font-size: 20px;
  }

  .slide-info p {
    font-size: 14px;
  }

  .slideshow-dots {
    bottom: 10px;
  }
}

/* 顶部操作栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 0;
  border-bottom: 2px solid var(--border-medium);
  margin-bottom: 30px;
}

.page-title h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: var(--primary-color);
  text-shadow: var(--shadow-sm);
}

.subtitle {
  margin: 0;
  color: var(--secondary-color);
  font-size: 14px;
  font-weight: 500;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 控制按钮样式 */
.controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-self: center; /* 垂直居中 */
  flex-shrink: 0; /* 防止被压缩 */
}

@media (max-width: 768px) {
  .controls {
    flex-direction: row;
    align-items: center;
    justify-content: space-between; /* 分散对齐，覆盖更多宽度 */
    gap: 0; /* 移除固定间距，使用justify-content控制 */
    margin: 0 auto; /* 水平居中 */
    margin-top: 10px; /* 距离上方内容有一定距离 */
    align-self: center; /* 在移动端居中 */
    width: 100%; /* 占满容器宽度 */
    max-width: 500px; /* 限制最大宽度，避免过宽 */
  }

  .controls .edit-movie-button,
  .controls .up-down-button {
    font-size: 18px; /* 稍微调小图标 */
    padding: 12px; /* 增加点击区域 */
    flex: 1; /* 让按钮平均分配空间 */
    max-width: 80px; /* 限制最大宽度，保持美观 */
  }

  .controls .edit-movie-button {
    order: 2; /* 编辑按钮放在中间 */
  }

  .controls .up-down-button:first-child {
    order: 1; /* 上移按钮放在左边 */
  }

  .controls .up-down-button:last-child {
    order: 3; /* 下移按钮放在右边 */
  }
}

.edit-movie-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: var(--primary-color);
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.edit-movie-button:hover {
  background-color: var(--bg-gradient-medium);
  transform: scale(1.05);
}

.up-down-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: var(--primary-color);
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.up-down-button:hover {
  background-color: var(--bg-gradient-medium);
  transform: scale(1.05);
}

.up-down-button:disabled {
  color: #ccc;
  cursor: not-allowed;
  background-color: transparent;
  transform: none;
}

.up-down-button:disabled:hover {
  background-color: transparent;
  transform: none;
}

.save-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--btn-primary-bg);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
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

/* 筛选器面板 */
.filter-panel {
  background: var(--bg-gradient-light);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 30px;
  border: 2px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-color);
}

/* 搜索区域 */
.search-section {
  margin-bottom: 24px;
}

.search-section .el-input {
  width: 100%;
}

/* 筛选器区域 */
.filters-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 14px;
}

.rating-slider-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rating-display {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 14px;
  min-width: 60px;
}

/* 筛选统计 */
.filter-stats {
  display: flex;
  justify-content: center;
  padding-top: 16px;
  border-top: 1px solid #e4e7ed;
}

.save-button:hover {
  background: var(--btn-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.save-button:active {
  transform: translateY(0);
  box-shadow: var(--shadow-md);
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

/* 响应式设计 */
@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }

  .page-title h1 {
    font-size: 24px;
  }

  .filter-panel {
    padding: 16px;
  }

  .filters-section {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .filter-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
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
