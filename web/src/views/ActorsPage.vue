<template>
  <div class="actors-container">
    <!-- 演员视图 -->
    <div class="actor-view">
      <h1>演员列表</h1>
      <div class="actor-grid">
        <div v-for="(actor, index) in actors" :key="actor.name" class="actor-item">
          <img
            :src="actor.cover"
            alt="演员封面"
            class="actor-cover"
            @click="goToActor(actor.name)"
            @error="setDefaultCover($event)"
          />
          <span class="actor-name">{{ actor.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ActorsPage',
  data() {
    return {
      actors: [],
      defaultCover: '/imgs/default_cover.jpg', // 默认封面图片路径
    }
  },
  methods: {
    goToActor(name) {
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
    },
    setDefaultCover(event) {
      event.target.src = this.defaultCover // 设置默认封面图片
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
  mounted() {
    this.fetchActors()
  },
}
</script>

<style scoped>
.actor-view {
  max-width: 1200px;
  justify-content: center; /* 水平居中 */
  margin: auto;
}

.actor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 40px;
  margin-top: 20px;
}

.actor-item {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 居中对齐 */
  text-align: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 不设置固定高度，让内容决定高度 */
}

.actor-cover {
  max-width: 200px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 10%; /* 圆形封面 */
}

.actor-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  word-wrap: break-word; /* 长名字自动换行 */
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

.new-button {
  margin: 20px 10px;
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
