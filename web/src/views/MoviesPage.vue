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

      <div v-for="(movie, index) in filteredMovies" :key="movie.id" class="movie-item">
        <!-- 封面 -->
        <div class="cover-wrapper" @click="goToDetail(movie.id)">
          <img :src="movie.cover" alt="封面" class="cover" @error="setDefaultCover($event)" />
        </div>
        <!-- 详细信息 -->
        <div class="details">
          <h2>{{ movie.title }}</h2>
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
            <span v-for="i in 5" :key="i" class="star" @click="setRating(movie, i)">
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
        </div>
        <!-- 上移/下移按钮 -->
        <div class="controls">
          <button @click="moveUp(index)" :disabled="index === 0" class="up-down-button">
            <el-icon><ArrowUp /></el-icon>
          </button>
          <button
            @click="moveDown(index)"
            :disabled="index === movies.length - 1"
            class="up-down-button"
          >
            <el-icon><ArrowDown /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 导入 Element Plus 图标
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

import axios from 'axios'
import { useViewStore } from '../store/view'

export default {
  name: 'MoviesPage',
  components: {
    ArrowUp,
    ArrowDown,
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
      }
    },
    setDefaultCover(event) {
      event.target.src = this.defaultCover // 设置为默认图片路径
    },
    goToDetail(id) {
      console.log('跳转到详情页，电影 ID:', id) // 调试信息
      // 使用 Vue Router 跳转到详情页
      this.$router.push({ name: 'MovieDetail', params: { id } }) // 跳转到详情页
    },
    goToActor(name) {
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

.movie-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

/* 宽屏设备：横向排列 */
@media (min-width: 768px) {
  .movie-item {
    flex-direction: row; /* 横向排列 */
  }
  .cover {
    max-width: 350px; /* 设置最大宽度，避免图片过大 */
    object-fit: cover; /* 确保图片填充整个区域，避免拉伸或变形 */
    aspect-ratio: 16 / 9; /* 设置宽高比为 16:9 */
    margin-right: 20px;
  }
  .details {
    flex: 1;
    text-align: left;
  }
  .controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
}

/* 窄屏设备：竖向排列 */
@media (max-width: 768px) {
  .movie-item {
    flex-direction: column; /* 竖向排列 */
    align-items: flex-start; /* 左对齐 */
  }
  .cover {
    max-width: 100%; /* 让封面占满容器宽度 */
    margin-right: 0; /* 移除右侧间距 */
    margin-bottom: 10px; /* 添加底部间距 */
  }
  .details {
    width: 100%; /* 占满容器宽度 */
    text-align: left;
  }
  .controls {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
}

.rating {
  display: flex;
  align-items: center;
  gap: 2px; /* 星星之间的间距 */
}

.star {
  font-size: 20px; /* 星星图标的大小 */
  color: #ccc; /* 默认颜色为灰色 */
}

.star .material-icons.filled {
  color: #ffca28; /* 填充的星星颜色为黄色 */
}

.star:hover {
  cursor: pointer; /* 鼠标悬停时显示为手型 */
}

.actor-tag {
  margin-right: 5px;
  cursor: pointer;
}

.tag-item {
  margin-right: 5px;
}

.tag-item:hover {
  cursor: pointer;
  background-color: #f0f0f0; /* 鼠标悬停时的背景色 */
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

.add-button {
  margin: 20px 10px;
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
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
</style>
