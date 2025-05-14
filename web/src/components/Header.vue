<template>
  <header :class="['app-header', isMobile ? 'mobile-header' : 'desktop-header']">
    <!-- 桌面端 Header -->
    <div v-if="!isMobile" class="desktop-header-content">
      <div class="header-wrapper">
        <div class="logo" @click="goToHome">
          <img src="/home-button.png" alt="Logo" />
        </div>
        <h1 class="title">影片排行榜</h1>
      </div>
      <div class="header-nav">
        <span @click="goToMovies" class="nav-link" title="影片排行页面">影片排行</span>
        <span @click="goToActors" class="nav-link" title="演员列表页面">演员列表</span>
        <span @click="goToTags" class="nav-link" title="标签页页面">标签列表</span>
      </div>
    </div>

    <!-- 移动端 Header -->
    <div v-else class="mobile-header-content">
      <div class="header-wrapper">
        <div class="logo" @click="goToHome">
          <img src="/home-button.png" alt="Logo" />
        </div>
        <h1 class="title">影片排行榜</h1>
        <button class="menu-button" @click="toggleMenu">
          <!-- 动态切换图标 -->
          <span class="material-icons">{{ isMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
      <div v-if="isMenuOpen" class="dropdown-menu">
        <span @click="goToMovies" class="nav-link" title="影片排行页面">影片排行</span>
        <span @click="goToActors" class="nav-link" title="演员列表页面">演员列表</span>
        <span @click="goToTags" class="nav-link" title="标签页页面">标签</span>
      </div>
    </div>
  </header>
</template>

<script>
import { useViewStore } from '../store/view'
export default {
  name: 'Header',
  data() {
    return {
      isMobile: false, // 是否显示菜单按钮
      isMenuOpen: false, // 菜单是否展开
    }
  },
  setup() {
    const viewStore = useViewStore()
    return { viewStore }
  },
  methods: {
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
      this.isMenuOpen = false // 关闭菜单
    },
    goToMovies() {
      this.$router.push({ name: 'MoviesPage' }) // 跳转到影片排行页面
      this.isMenuOpen = false // 关闭菜单
    },
    goToActors() {
      this.$router.push({ name: 'ActorsPage' }) // 跳转到演员列表页面
      this.isMenuOpen = false // 关闭菜单
    },
    goToTags() {
      this.$router.push('/tags') // 跳转到标签页面
      this.isMenuOpen = false // 关闭菜单
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen // 切换菜单状态
    },
    checkScreenWidth() {
      this.isMobile = window.innerWidth < 768 // 当屏幕宽度小于 768px 时显示菜单按钮 [[1]]
    },
    toggleView() {
      this.viewStore.toggleView()
    },
  },
  created() {
    this.checkScreenWidth() // 初始化检查屏幕宽度
    window.addEventListener('resize', this.checkScreenWidth) // 监听窗口大小变化
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkScreenWidth) // 移除监听器
  },
}
</script>

<style scoped>
.app-header {
  background-color: #f8f8f8;
  padding: 10px 0 0 0;
  align-items: center;
  display: flex;
}

.header-wrapper {
  display: flex;
  align-items: left;
}

.logo img {
  width: 50px;
  cursor: pointer;
  margin-left: 10px;
}

.title {
  color: black;
  font-size: 24px;
  margin: 10px 20px;
}

.menu-button {
  background-color: transparent;
  border: none;
  color: black;
  font-size: 18px;
  cursor: pointer;
  margin-left: auto; /* 将菜单按钮推到右侧 */
}

.toggle-icon {
  font-size: 24px;
  cursor: pointer;
  margin-right: 10px;
  color: #999;
}
.toggle-icon.active {
  color: #42b983; /* 高亮当前选中的图标 */
}

.toggle-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-left: auto;
}
.toggle-button:hover {
  background-color: #33a07c;
}

.material-icons {
  font-size: 24px; /* 设置图标的大小 */
}

/* 桌面端 Header 样式 */
.desktop-header-content {
  display: flex;
  align-items: center;
  width: 100%; /* 占满整个 Header 宽度 */
  justify-content: space-between; /* 左右两侧对齐 */
}

.header-nav {
  margin-right: 20px; /* 设置右侧间距 */
  gap: 20px; /* 设置导航链接之间的间距 */
  display: flex; /* 水平排列 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.header-nav .nav-link {
  color: black; /* 设置文字颜色为黑色 [[7]] */
  text-decoration: none; /* 去掉下划线 */
  font-size: 16px;
  cursor: pointer; /* 显示手型光标 */
}

.header-nav .nav-link:hover {
  text-decoration: underline; /* 鼠标悬停时添加下划线 */
}

.mobile-header-content {
  width: 100%; /* 占满整个 Header 宽度 */
}

/* 下拉菜单样式 */
.dropdown-menu {
  margin-top: 20px; /* 下拉菜单距离按钮的距离 */
  width: 100%; /* 占满整个 Header 宽度 */
  display: flex; /* 展开时显示 */
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 居中对齐 */
  border-top: 2px solid #f0f0f0; /* 上边框颜色 */
}

.dropdown-menu .nav-link {
  padding: 10px;
  color: black;
  text-align: center;
}

.dropdown-menu .nav-link:hover {
  color: #42b983; /* 鼠标悬停时改变颜色 */
}
</style>
