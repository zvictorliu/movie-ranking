<template>
  <div id="app">
    <!-- 全局头部 -->
    <AppHeader />

    <!-- 路由视图：显示当前路由对应的页面 -->
    <main class="app-main">
      <router-view :key="$route.fullPath"></router-view>
      <!-- 强制重新渲染组件 [[4]] -->
    </main>

    <!-- 全局底部 -->
    <AppFooter />

    <!-- 图片侧边栏 -->
    <ImageSidebar />

    <!-- 新建菜单（仅移动端） -->
    <CreateMenu />
  </div>
</template>

<script>
import AppFooter from './components/AppFooter.vue'
import AppHeader from './components/AppHeader.vue'
import ImageSidebar from './components/ImageSidebar.vue'
import CreateMenu from './components/CreateMenu.vue'
import { useViewStore } from './store/view'
import './assets/material-icons.scss'
export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    ImageSidebar,
    CreateMenu,
  },
  setup() {
    const viewStore = useViewStore()
    return { viewStore }
  },
}
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
}

/* 夜间模式 */
body.dark-mode {
  background-color: #292a2d;
  color: #a9a9b3;
}
</style>
