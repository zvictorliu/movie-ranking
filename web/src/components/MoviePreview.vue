<template>
  <div class="movie-preview" v-if="movie">
    <div class="movie-item">
      <!-- 封面 -->
      <div class="cover-wrapper" @click="goToDetail(movie.id)">
        <img :src="movie.cover" alt="封面" class="movie-cover" @error="setDefaultCover($event)" />
      </div>
      <!-- 详细信息 -->
      <div class="details">
        <h2>{{ movie.title }}</h2>
        <!-- 评分 -->
        <div class="rating">
          <strong>评分：</strong>
          <div class="stars-container">
            <span
              v-for="i in 5"
              :key="i"
              class="star-wrapper"
              :class="{
                clickable: allowRating && !ratingUpdating,
                'hover-effect': allowRating && i <= movie.rating,
                updating: ratingUpdating,
              }"
              :title="allowRating ? `点击评分 ${i} 星` : ''"
              @click="handleRatingClick(i)"
              @mouseenter="allowRating && handleStarHover(i)"
              @mouseleave="allowRating && handleStarLeave()"
            >
              <span
                class="material-icons star-icon"
                :class="{
                  filled: i <= movie.rating,
                  hover: allowRating && i <= hoverRating,
                }"
              >
                {{ i <= movie.rating ? 'star' : 'star_border' }}
              </span>
            </span>
          </div>
        </div>
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
      <!-- 插槽：用于添加额外的控制按钮 -->
      <slot name="controls"></slot>
    </div>
  </div>
  <div v-else class="loading">
    <p>加载中...</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MoviePreview',
  props: {
    title: {
      type: String,
      required: true,
    },
    // 新增：是否允许点击评分
    allowRating: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      movie: null,
      loading: false,
      error: null,
      hoverRating: 0, // 鼠标悬停时的评分
      ratingUpdating: false, // 评分更新状态
    }
  },
  async created() {
    await this.fetchMovie(this.title)
  },
  watch: {
    title: {
      handler() {
        this.fetchMovie(this.title)
      },
      immediate: true,
    },
  },
  mounted() {
    // 监听影片创建事件，因为可能会影响当前影片信息
    this.$eventBus.on('movie-created', () => {
      this.fetchMovie(this.title)
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('movie-created')
  },
  methods: {
    async fetchMovie(title) {
      this.loading = true
      this.error = null

      try {
        // 直接使用现有的 API 接口，id 和 movie_name 通常是一样的
        const response = await axios.get(`/api/movie/${title}`)
        this.movie = response.data
      } catch (error) {
        console.error('获取电影信息失败:', error)
        this.error = '获取电影信息失败'
        this.movie = null
      } finally {
        this.loading = false
      }
    },
    setDefaultCover(event) {
      event.target.src = '/imgs/default_cover.jpg'
    },
    goToDetail(id) {
      if (id) {
        this.$router.push({ name: 'MovieDetail', params: { id } })
      }
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
    goToActor(name) {
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
    },
    // 新增：处理评分点击
    async handleRatingClick(rating) {
      if (this.allowRating && !this.ratingUpdating) {
        this.ratingUpdating = true

        // 添加点击动画效果
        const starElement = event.target.closest('.star-wrapper')
        if (starElement) {
          starElement.style.transform = 'scale(1.2)'
          setTimeout(() => {
            starElement.style.transform = ''
          }, 150)
        }

        try {
          // 调用专门的评分更新API
          await this.updateMovieRating(rating)

          this.$message.success('评分已更新！')
        } catch (error) {
          console.error('评分更新失败:', error)
          this.$message.error('评分更新失败，请稍后再试！')
        } finally {
          // 重置更新状态
          setTimeout(() => {
            this.ratingUpdating = false
          }, 500)
        }
      }
    },
    // 新增：更新电影评分的API调用
    async updateMovieRating(rating) {
      const response = await axios.put(`/api/update-movie-rating/${this.movie.id}`, {
        rating: rating,
      })

      if (response.data.success) {
        // 更新本地数据
        this.movie.rating = rating
        return response.data
      } else {
        throw new Error('评分更新失败')
      }
    },
    // 处理星星悬停效果
    handleStarHover(rating) {
      this.hoverRating = rating
    },
    // 处理星星离开效果
    handleStarLeave() {
      this.hoverRating = 0
    },
  },
}
</script>

<style scoped>
.movie-preview {
  width: 100%;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.movie-item {
  display: flex;
  align-items: center; /* 改为center以便垂直居中 */
  justify-content: space-between; /* 添加空间分布 */
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.movie-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.cover-wrapper {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.cover-wrapper:hover {
  transform: scale(1.05);
}

.details h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.5em;
}

/* 宽屏设备：横向排列 */
@media (min-width: 768px) {
  .movie-item {
    flex-direction: row;
  }
  .movie-cover {
    max-width: 350px;
    object-fit: cover;
    aspect-ratio: 16 / 9;
    margin-right: 20px;
    border-radius: 8px;
  }
  .details {
    flex: 1;
    text-align: left;
    margin-right: 20px; /* 为controls留出空间 */
  }
}

/* 窄屏设备：竖向排列 */
@media (max-width: 768px) {
  .movie-item {
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* 内容从顶部开始 */
  }
  .movie-cover {
    max-width: 100%;
    margin-right: 0;
    margin-bottom: 15px;
    border-radius: 8px;
  }
  .details {
    width: 100%;
    text-align: left;
    margin-right: 0; /* 移除右边距 */
  }
}

.rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 12px 0;
  flex-wrap: wrap; /* 允许换行 */
}

.rating strong {
  white-space: nowrap; /* 防止标签文字换行 */
  flex-shrink: 0; /* 防止标签被压缩 */
}

.stars-container {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0; /* 防止星星容器被压缩 */
}

.star-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.star-wrapper.clickable {
  cursor: pointer;
}

.star-wrapper.clickable:hover {
  background-color: rgba(255, 202, 40, 0.1);
  transform: scale(1.1);
}

.star-wrapper.hover-effect {
  background-color: rgba(255, 202, 40, 0.05);
}

.star-wrapper.updating {
  opacity: 0.6;
  pointer-events: none;
}

.star-wrapper.updating .star-icon {
  animation: pulse 1s infinite;
}

.star-icon {
  font-size: 24px;
  color: #ddd;
  transition: all 0.2s ease;
  user-select: none;
}

.star-icon.filled {
  color: #ffca28;
  text-shadow: 0 0 8px rgba(255, 202, 40, 0.3);
}

.star-icon.hover {
  color: #ffd54f;
  text-shadow: 0 0 12px rgba(255, 202, 40, 0.5);
  transform: scale(1.05);
}

.star-wrapper.clickable:hover .star-icon {
  color: #ffd54f;
  text-shadow: 0 0 12px rgba(255, 202, 40, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .rating {
    flex-direction: row; /* 保持横向排列 */
    align-items: center;
    gap: 6px; /* 稍微减少间距 */
    flex-wrap: wrap; /* 允许换行，但优先保持并列 */
  }

  .stars-container {
    gap: 1px;
  }

  .star-wrapper {
    padding: 2px; /* 减少内边距 */
  }
}

/* 极窄屏幕优化 */
@media (max-width: 480px) {
  .rating {
    gap: 4px; /* 进一步减少间距 */
  }

  .star-wrapper {
    padding: 1px; /* 最小内边距 */
  }
}

/* 深色模式支持 */
body.dark-mode .star-icon {
  color: #555;
}

/* 动画定义 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.tag-item {
  margin-right: 5px;
  border-radius: 12px;
}

.tag-item:hover {
  color: #333;
  text-decoration: none;
  cursor: pointer;
}
</style>
