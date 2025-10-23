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

    // 监听影片和博客创建事件，因为可能会添加新标签
    this.$eventBus.on('movie-created', () => {
      this.fetchTags()
    })

    this.$eventBus.on('post-created', () => {
      this.fetchTags()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('movie-created')
    this.$eventBus.off('post-created')
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
  padding: 20px;
}

.tags-page h1 {
  color: var(--primary-color);
  font-size: 32px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: var(--shadow-sm);
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px; /* 设置标签之间的间距 */
  margin-top: 20px;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  padding: 10px 18px;
  border: 2px solid var(--border-medium);
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--bg-gradient-light);
  box-shadow: var(--shadow-sm);
}

.tag-item:hover {
  transform: translateY(-2px) scale(1.05);
  border-color: var(--primary-color);
  background: var(--bg-gradient-medium);
  box-shadow: var(--shadow-hover);
}

.tag-name {
  margin-right: 8px;
  color: var(--primary-color);
  font-weight: 500;
}

.tag-count {
  color: var(--secondary-color);
  font-size: 12px;
  font-weight: 600;
  background: var(--bg-gradient-light);
  padding: 2px 8px;
  border-radius: 10px;
}
</style>
