<template>
  <div id="app">
    <!-- 全局头部 -->
    <AppHeader v-if="!hideChrome" />

    <!-- 路由视图：显示当前路由对应的页面 -->
    <main class="app-main" :class="{ 'app-main--chrome-free': hideChrome }">
      <router-view :key="$route.fullPath"></router-view>
      <!-- 强制重新渲染组件 [[4]] -->
    </main>

    <!-- 全局底部 -->
    <AppFooter v-if="!hideChrome" />

    <!-- 图片侧边栏 -->
    <ImageSidebar v-if="!hideChrome" />

    <!-- 新建菜单（仅移动端） -->
    <CreateMenu v-if="!hideChrome" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
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
    const route = useRoute()
    const hideChrome = computed(() => Boolean(route.meta.hideChrome))
    return { viewStore, hideChrome }
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

.app-main--chrome-free {
  min-height: 100vh;
}

/* 夜间模式 */
body.dark-mode {
  background-color: #292a2d;
  color: #a9a9b3;
}
</style>
