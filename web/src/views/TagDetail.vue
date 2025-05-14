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
  max-width: 800px;
  margin: auto;
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
  .movie-cover {
    max-width: 350px; /* 设置最大宽度，避免图片过大 */
    object-fit: cover; /* 确保图片填充整个区域，避免拉伸或变形 */
    aspect-ratio: 16 / 9; /* 设置宽高比为 16:9 */
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
    flex-direction: column; /* 竖向排列 */
    align-items: flex-start; /* 左对齐 */
  }
  .movie-cover {
    max-width: 100%; /* 让封面占满容器宽度 */
    margin-right: 0; /* 移除右侧间距 */
    margin-bottom: 10px; /* 添加底部间距 */
  }
  .details {
    width: 100%; /* 占满容器宽度 */
    text-align: left;
  }
}

.no-movies {
  text-align: center;
  font-size: 18px;
  color: #999;
  margin-top: 20px;
}
</style>
