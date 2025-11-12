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
  --tag-title-gradient: var(--primary-gradient);
}

.tag-detail-page h1 {
  color: var(--primary-color);
  font-size: 2.5rem;
  margin-bottom: 30px;
  text-align: center;
  background: var(--tag-title-gradient);
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
  color: var(--primary-color);
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
  background: var(--bg-gradient-light);
  border: 1px solid var(--border-light);
  padding: 15px;
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
  cursor: pointer;
}

.movie-item:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-3px);
  border-color: var(--primary-color);
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
  border: 2px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}

.details h2 {
  color: var(--primary-color);
  font-size: 1.5rem;
  margin-bottom: 15px;
  background: var(--tag-title-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.details p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.details strong {
  color: var(--primary-color);
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
  color: var(--text-muted);
  margin-top: 40px;
  padding: 30px;
  background: var(--bg-gradient-light);
  border-radius: 12px;
  border: 1px solid var(--border-light);
}
</style>

<style>
body.theme-minimal.dark-mode .tag-detail-page {
  --tag-title-gradient: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.95) 0%,
    rgba(224, 224, 224, 0.85) 100%
  );
}
</style>
