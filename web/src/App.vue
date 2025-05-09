<template>
  <div id="app">
    <!-- 全局头部 -->
    <Header />

    <!-- 路由视图：显示当前路由对应的页面 -->
    <main class="app-main">
      <router-view :key="$route.fullPath"></router-view>
      <!-- 强制重新渲染组件 [[4]] -->
    </main>

    <!-- 全局底部 -->
    <Footer />
    
  </div>
</template>

<script>
import Footer from "./components/Footer.vue";
import Header from "./components/Header.vue";
export default {
  name: "App",
  components: {
    Header,
    Footer,
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

.app-main {
  flex: 1;
  padding: 20px;
}

</style>
