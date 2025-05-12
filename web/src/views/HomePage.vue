<template>
  <div class="home-page">
    <!-- 背景容器 -->
    <div class="welcome-container">
      <h1 class="welcome-title">欢迎来到影片排行榜网站</h1>
      <p class="welcome-description">
        这里为你提供最新的影片排行和演员信息，快来探索吧！
      </p>
      <div class="welcome-buttons">
        <button class="welcome-button" @click="goToMovies">查看影片排行</button>
        <button class="welcome-button" @click="goToActors">查看演员列表</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    goToMovies() {
      this.$router.push('/movies'); // 跳转到影片排行榜页面 
    },
    goToActors() {
      this.$router.push('/actors'); // 跳转到演员列表页面 
    },
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 占满整个屏幕高度 */
  background: url('/background.jpg') no-repeat center center/cover; /* 背景图片 */
  color: white;
  text-align: center;
}

.welcome-container {
  padding: 20px;
  max-width: 600px; /* 限制内容宽度 */
  background-color: rgba(0, 0, 0, 0.7); /* 半透明背景 */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.welcome-title {
  font-size: 36px;
  margin-bottom: 20px;
}

.welcome-description {
  font-size: 18px;
  margin-bottom: 30px;
}

.welcome-buttons {
  display: flex;
  gap: 20px; /* 按钮之间的间距 */
  justify-content: center;
}

.welcome-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s ease; /* 添加过渡效果 */
}

.welcome-button:hover {
  background-color: #33a07c; /* 鼠标悬停时改变颜色 */
}
</style>