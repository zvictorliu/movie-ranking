<template>
  <div class="movies-container">
    <!-- 影片视图 -->
    <div class="movie-view">
      <button @click="saveRanking" class="save-button material-icons" title="保存">save</button>
      <!-- 筛选器 -->
      <div class="filter-container">
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

      <MoviePreview
        v-for="(movie, index) in filteredMovies"
        :key="movie.id"
        :title="movie.title"
        :allow-rating="true"
        @rating-changed="setRating"
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
import { ArrowUp, ArrowDown, EditPen } from '@element-plus/icons-vue'

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
      ratingRange: [3, 5], // 默认评分区间
      defaultCover: '/imgs/default_cover.jpg', // 默认封面图片路径
      editDialogVisible: false, // 控制编辑对话框的显示状态
      editFormData: {}, // 当前正在编辑的影片数据
    }
  },
  methods: {
    setRating(movie, rating) {
      movie.rating = rating // 更新当前影片的评分
    },
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
      if (this.selectedActors.length > 0) {
        this.filteredMovies = this.movies.filter((movie) =>
          this.selectedActors.some(
            (actor) => movie.actors && movie.actors.split(', ').includes(actor),
          ),
        )
      } else {
        this.filteredMovies = [...this.movies] // 如果未选择演员，则显示所有影片
      }

      // 再根据评分区间筛选
      if (this.ratingRange[0] >= 0 || this.ratingRange[1] <= 5) {
        filtered = this.filteredMovies.filter(
          (movie) => movie.rating >= this.ratingRange[0] && movie.rating <= this.ratingRange[1],
        )
      }

      this.filteredMovies = filtered
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
      const newRanking = this.filteredMovies.map((movie, index) => ({
        id: movie.id,
        order: index + 1, // 更新顺序值
        rating: movie.rating || 0, // 如果没有评分，默认为 0
      }))
      try {
        await axios.post('/api/update-ranking', { ranking: newRanking })
        this.$message.success('排行已更新！')
        this.fetchMovies() // 重新获取影片列表
      } catch (error) {
        console.error('Error updating ranking:', error)
        this.$message.error('更新失败，请稍后再试！')
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
  justify-content: center; /* 水平居中 */
  margin: auto;
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
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
.save-button:hover {
  background-color: #33a07c;
}

.filter-container {
  margin-bottom: 20px;
  align-items: left;
  display: flex;
  flex-direction: column;
}
.filter-container label {
  margin-right: 10px;
}
.filter-container select {
  margin-left: 10px;
}

.rating-filter {
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-left: 0;
}

.rating-filter span {
  margin-left: 10px;
}

body.dark-mode .save-button {
  background-color: #3a3a3a; /* 夜间模式按钮颜色 */
  color: #a9a9b3;
}
</style>
