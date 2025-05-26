<template>
  <div class="tags-page">
    <h1>标签列表</h1>
    <div class="tag-list">
      <div
        v-for="(tag, index) in tags"
        :key="index"
        class="tag-item"
        @click="goToTagDetail(tag.tag)"
      >
        <span class="tag-name">{{ tag.tag }}</span>
        <span class="tag-count">{{ tag.count }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tags: [], // 标签列表
    }
  },
  async created() {
    await this.fetchTags()
  },
  methods: {
    async fetchTags() {
      try {
        const response = await axios.get('/api/tags') // 请求标签数据
        this.tags = response.data
      } catch (error) {
        console.error('Error fetching tags:', error)
      }
    },
    goToTagDetail(tagName) {
      this.$router.push(`/tags/${tagName}`) // 跳转到标签详情页面
    },
  },
}
</script>

<style scoped>
.tags-page {
  max-width: 800px;
  justify-content: center; /* 水平居中 */
  margin: auto;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* 设置标签之间的间距 */
  margin-top: 20px;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border: 1px solid #ddd; /* 添加边框，无背景 */
  border-radius: 4px; /* 轻微圆角，提升美观性 */
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.3s ease; /* 添加放大效果的过渡动画 */
}

.tag-item:hover {
  transform: scale(1.1); /* 鼠标悬停时放大 */
}

.tag-name {
  margin-right: 6px; /* 名称和数量之间的间距 */
}

.tag-count {
  color: #999; /* 数量颜色为灰色 */
  font-size: 12px; /* 数量字体稍小 */
}
</style>
