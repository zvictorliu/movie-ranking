<template>
  <div class="tag-detail-page">
    <h1>标签: {{ tagName }}</h1>
    <div v-if="movies.length > 0" class="movie-list">
      <div v-for="movie in movies" :key="movie.id" class="movie-item">
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
            <span v-for="i in 5" :key="i" class="star">
              <span class="material-icons" :class="{ filled: i <= movie.rating }">
                {{ i <= movie.rating ? 'star' : 'star_border' }}
              </span>
            </span>
          </div>

          <!-- 简介 -->
          <p><strong>简介：</strong>{{ movie.description }}</p>
        </div>
      </div>
    </div>
    <p v-else>暂无相关影片。</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tagName: '', // 当前标签名称
      movies: [], // 包含该标签的影片列表
    }
  },
  async created() {
    this.tagName = this.$route.params.tagName // 获取路由参数中的标签名称
    await this.fetchMoviesByTag()

    // 监听影片创建事件，因为可能会添加包含当前标签的新影片
    this.$eventBus.on('movie-created', () => {
      this.fetchMoviesByTag()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('movie-created')
  },
  methods: {
    async fetchMoviesByTag() {
      try {
        const response = await axios.get(`/api/tags/${this.tagName}`) // 请求包含该标签的影片数据
        this.movies = response.data
      } catch (error) {
        console.error('Error fetching movies by tag:', error)
      }
    },
    async goToDetail(id) {
      try {
        this.$router.push({ name: 'MovieDetail', params: { id } })
      } catch (error) {
        console.error('电影记录不存在:', error)
        alert('不存在对应的电影记录')
      }
    },
    setDefaultCover(event) {
      event.target.src = '/imgs/default.jpg' // 设置默认封面
    },
  },
}
</script>

<style scoped>
.tag-detail-page {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}

.tag-detail-page h1 {
  color: #667eea;
  font-size: 2.5rem;
  margin-bottom: 30px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.movie-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 10px;
}

.rating strong {
  color: #667eea;
  margin-right: 5px;
}

.star {
  font-size: 20px;
  color: #ddd;
  transition: all 0.2s ease;
}

.star .material-icons.filled {
  color: #ffca28;
  text-shadow: 0 2px 4px rgba(255, 202, 40, 0.3);
}

.movie-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 1px solid rgba(102, 126, 234, 0.2);
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.movie-item:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
  transform: translateY(-3px);
  border-color: #667eea;
}

.cover-wrapper {
  cursor: pointer;
  transition: all 0.3s ease;
}

.cover-wrapper:hover {
  transform: scale(1.02);
}

.movie-cover {
  border-radius: 8px;
  border: 2px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.details h2 {
  color: #667eea;
  font-size: 1.5rem;
  margin-bottom: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.details p {
  color: #555;
  line-height: 1.6;
}

.details strong {
  color: #667eea;
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
  }
  .details {
    flex: 1;
    text-align: left;
  }
}

/* 窄屏设备：竖向排列 */
@media (max-width: 768px) {
  .movie-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .movie-cover {
    max-width: 100%;
    margin-right: 0;
    margin-bottom: 15px;
  }
  .details {
    width: 100%;
    text-align: left;
  }
  .tag-detail-page h1 {
    font-size: 2rem;
  }
}

.no-movies {
  text-align: center;
  font-size: 18px;
  color: #999;
  margin-top: 40px;
  padding: 30px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

/* 暗色模式 */
body.dark-mode .tag-detail-page h1 {
  background: linear-gradient(135deg, #a8b5f0 0%, #c8a5d8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

body.dark-mode .movie-item {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

body.dark-mode .movie-item:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  border-color: #a8b5f0;
}

body.dark-mode .movie-cover {
  border-color: rgba(168, 181, 240, 0.3);
}

body.dark-mode .details h2 {
  background: linear-gradient(135deg, #a8b5f0 0%, #c8a5d8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

body.dark-mode .details p {
  color: #b0b0b0;
}

body.dark-mode .details strong {
  color: #a8b5f0;
}

body.dark-mode .rating strong {
  color: #a8b5f0;
}

body.dark-mode .no-movies {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.2);
  color: #b0b0b0;
}
</style>
