<template>
  <div class="actor-detail">
    <h1>{{ actor.name }}</h1>
    <img :src="actor.cover" alt="演员封面" class="cover" @error="setDefaultCover($event)" />
    <p><strong>出生日期：</strong>{{ actor.birth }}</p>
    <p><strong>出道日期：</strong>{{ actor.debut }}</p>

    <!-- 渲染移除了“主要作品”部分的完整内容 -->
    <div v-html="filteredBodyHtml" class="content"></div>

    <!-- 主要作品 -->
    <h2>主要作品</h2>
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
          <p><strong>简介：</strong>{{ movie.description }}</p>
        </div>
      </div>
    </div>
    <p v-else>暂无主要作品信息</p>

    <!-- 返回按钮 -->
    <button @click="goBack">返回</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ActorDetailPage',
  data() {
    return {
      actor: {},
      movies: [], // 存储主要作品的影片信息
      filteredBodyHtml: '', // 移除了“主要作品”部分的完整内容
    }
  },
  async created() {
    const { name } = this.$route.params
    try {
      const response = await axios.get(`/api/actor/${name}`)
      this.actor = response.data

      // 提取并移除“主要作品”部分
      this.filteredBodyHtml = this.removeMainWorksSection(this.actor.body_html)

      // 提取主要作品部分的条目
      const mainWorks = this.extractMainWorks(this.actor.body_html)
      // 根据条目请求影片信息
      this.movies = await Promise.all(
        mainWorks.map(async (movieName) => {
          const movieResponse = await axios.get(`/api/movie/${movieName}`)
          return movieResponse.data
        }),
      )
    } catch (error) {
      console.error('请求失败:', error)
    }
  },
  methods: {
    setDefaultCover(event) {
      event.target.src = '/imgs/default_cover.jpg'
    },
    goBack() {
      this.$router.go(-1) // 返回上一页 [[7]]
    },
    async goToDetail(id) {
      try {
        this.$router.push({ name: 'MovieDetail', params: { id } })
      } catch (error) {
        console.error('电影记录不存在:', error)
        alert('不存在对应的电影记录')
      }
    },
    extractMainWorks(html) {
      const parser = new DOMParser()
      const doc = parser.parseFromString(html, 'text/html') // 将 HTML 字符串解析为 DOM

      // 查找 <h2> 标签，匹配“主要作品”
      const mainWorksHeading = Array.from(doc.querySelectorAll('h2')).find(
        (h2) => h2.textContent.trim() === '主要作品',
      )
      if (!mainWorksHeading) return []

      // 获取 <h2> 后的下一个兄弟节点，直到遇到下一个 <h2> 或文档结束
      const items = []
      let sibling = mainWorksHeading.nextElementSibling
      while (sibling && sibling.tagName !== 'H2') {
        if (sibling.tagName === 'UL') {
          // 提取 <ul> 中的所有 <li> 内容
          sibling.querySelectorAll('li').forEach((li) => {
            items.push(li.textContent.trim())
          })
        }
        sibling = sibling.nextElementSibling
      }

      return items
    },
    removeMainWorksSection(html) {
      const parser = new DOMParser()
      const doc = parser.parseFromString(html, 'text/html')

      const mainWorksHeading = Array.from(doc.querySelectorAll('h2')).find(
        (h2) => h2.textContent.trim() === '主要作品',
      )
      if (!mainWorksHeading) {
        console.log('No "主要作品" section found.')
        return html
      }

      const parent = mainWorksHeading.parentNode
      let sibling = mainWorksHeading

      while (sibling) {
        const nextSibling = sibling.nextElementSibling

        // 如果遇到下一个 <h2> 或到达文档末尾，停止删除
        if (nextSibling && nextSibling.tagName === 'H2') break

        // 删除当前节点
        // console.log('Removing node:', sibling.outerHTML) // 打印正在删除的节点
        parent.removeChild(sibling)

        // 移动到下一个兄弟节点
        sibling = nextSibling
      }

      const modifiedHtml = doc.body.innerHTML
      return modifiedHtml
    },
  },
}
</script>

<style scoped>
.actor-detail {
  text-align: left;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.cover {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
}

.content ::v-deep(img) {
  /* 深度选择器，确保样式应用于子组件的 img 元素 */
  max-width: 100%; /* 确保图片宽度不超过父容器 */
  height: auto; /* 保持图片比例 */
  border-radius: 10px; /* 添加圆角效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 [[8]] */
}

button {
  padding: 10px 20px;
  cursor: pointer;
  position: relative;
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
</style>
