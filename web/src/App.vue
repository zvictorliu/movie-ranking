<template>
  <div id="app">
    <!-- 全局头部 -->
    <header class="app-header">
      <div class="logo" @click="goToHome">
        <img src="/home-button.png" alt="Logo" />
      </div>
      <h1 class="title" >影片排行榜</h1>
    </header>

    <!-- 路由视图：显示当前路由对应的页面 -->
    <main class="app-main">
      <router-view :key="$route.fullPath"></router-view>
      <!-- 强制重新渲染组件 [[4]] -->
    </main>

    <!-- 全局底部 -->
    <footer class="app-footer">
      <p>&copy; 2025 My Movie Ranking App</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
  methods: {
    goToHome() {
      this.$router.push({ name: "HomePage" }); // 返回主页 [[6]]
    },
  },
};
</script>

<style>
/* 全局样式 */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #42b983;
  padding: 10px 20px;
  align-items: center;
  display: flex;
}

.logo img {
  width: 50px;
  cursor: pointer;
}

.title {
  color: white;
  font-size: 24px;
  margin-left: 20px;
}

.app-main {
  flex: 1;
  padding: 20px;
}

.app-footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 10px;
}
</style>
