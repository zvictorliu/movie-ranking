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
        <button class="new-button" @click="openMovieDialog">新增影片</button>
        <button class="new-button" @click="openActorDialog">新增演员</button>
        <button class="theme-toggle" @click="toggleTheme">
          <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>
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
        <button class="new-button" @click="openMovieDialog">新增影片</button>
        <button class="new-button" @click="openActorDialog">新增演员</button>
        <button class="theme-toggle" @click="toggleTheme">
          <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>
      </div>
    </div>

    <!-- 浮动窗口 -->
    <el-dialog v-model="movieDialogVisible" title="新增影片" width="80%">
      <el-form :model="movieFormData" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="movieFormData.title" placeholder="请输入影片标题"></el-input>
        </el-form-item>
        <el-form-item label="演员">
          <el-input v-model="movieFormData.actors" placeholder="请输入演员，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="movieFormData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="movieFormData.description"
            type="textarea"
            placeholder="请输入影片简介"
          ></el-input>
        </el-form-item>
        <!-- <el-form-item label="封面">
            <el-input v-model="movieFormData.cover" placeholder="请输入封面图片路径"></el-input>
          </el-form-item> -->
        <el-form-item label="order">
          <el-input v-model="movieFormData.order" placeholder="请输入影片顺序"></el-input>
        </el-form-item>
        <el-form-item label="rating">
          <el-input v-model="movieFormData.rating" placeholder="请输入影片评分"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="movieDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMovie">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 浮动窗口 -->
    <el-dialog v-model="actorDialogVisible" title="新增演员" width="80%">
      <el-form :model="actorFormData" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="actorFormData.name" placeholder="请输入演员姓名"></el-input>
        </el-form-item>
        <el-form-item label="出生日期">
          <el-input
            v-model="actorFormData.birth"
            placeholder="请输入出生日期"
            style="width: 100%"
          ></el-input>
        </el-form-item>
        <el-form-item label="出道日期">
          <el-input
            v-model="actorFormData.debut"
            placeholder="请输入出道日期"
            style="width: 100%"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="actorDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveActor">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </header>
</template>

<script>
import { useViewStore } from '../store/view'
import axios from 'axios'
export default {
  name: 'Header',
  data() {
    return {
      isMobile: false, // 是否显示菜单按钮
      isMenuOpen: false, // 菜单是否展开
      isDarkMode: false, // 是否启用夜间模式
      movieDialogVisible: false, // 控制浮动窗口的显示状态
      movieFormData: {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 10,
        rating: 0,
      },
      actorDialogVisible: false, // 控制浮动窗口的显示状态
      actorFormData: {
        name: '',
        birth: '',
        debut: '',
      },
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
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode // 切换夜间模式
      document.body.classList.toggle('dark-mode', this.isDarkMode) // 动态切换 body 的主题类 [[7]]
    },
    checkScreenWidth() {
      this.isMobile = window.innerWidth < 768 // 当屏幕宽度小于 768px 时显示菜单按钮 [[1]]
    },
    toggleView() {
      this.viewStore.toggleView()
    },
    openMovieDialog() {
      this.movieDialogVisible = true // 打开浮动窗口
    },
    resetMovieForm() {
      this.movieFormData = {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 1,
        rating: 0,
      }
    },
    openActorDialog() {
      this.actorDialogVisible = true
    },
    resetActorForm() {
      this.actorFormData = {
        name: '',
        birth: '',
        debut: '',
      }
    },
    async saveMovie() {
      try {
        const response = await axios.post('/api/create-movie', this.movieFormData)
        if (response.data.success) {
          this.$message.success('影片已成功创建！')
          this.movieDialogVisible = false // 关闭浮动窗口
          this.resetMovieForm() // 清空表单
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
    async saveActor() {
      try {
        const response = await axios.post('/api/create-actor', this.actorFormData)
        if (response.data.success) {
          this.$message.success('演员已成功创建！')
          this.actorDialogVisible = false // 关闭浮动窗口
          this.resetActorForm() // 清空表单
        } else {
          this.$message.error('创建失败，请稍后再试！')
          console.error('Error details:', response.data.message)
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
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

.theme-toggle {
  background-color: transparent;
  border: none;
  color: black;
  font-size: 24px;
  cursor: pointer;
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

.header-nav .nav-link,
.header-nav .new-button {
  color: black; /* 设置文字颜色为黑色 [[7]] */
  text-decoration: none; /* 去掉下划线 */
  font-size: 16px;
  cursor: pointer; /* 显示手型光标 */
  background-color: transparent; /* 设置背景颜色为透明 */
  border: none; /* 去掉边框 */
  padding: 0;
}

.header-nav .nav-link:hover,
.header-nav .new-button:hover {
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
  gap: 10px; /* 设置下拉菜单项之间的间距 */
}

.dropdown-menu .nav-link,
.dropdown-menu .new-button {
  padding: 10px;
  color: black;
  text-align: center;
  background-color: transparent; /* 设置背景颜色为透明 */
  border: none; /* 去掉边框 */
  padding: 0;
  font-size: medium;
}

.dropdown-menu .nav-link:hover,
.dropdown-menu .new-button:hover {
  color: #42b983; /* 鼠标悬停时改变颜色 */
}

body.dark-mode .title {
  color: #a9a9b3;
}

body.dark-mode .app-header {
  background-color: #252627;
}

body.dark-mode .header-nav .nav-link,
body.dark-mode .header-nav .new-button,
body.dark-mode .theme-toggle {
  color: #a9a9b3;
}

body.dark-mode .dropdown-menu .nav-link,
body.dark-mode .dropdown-menu .new-button,
body.dark-mode .menu-button {
  color: #a9a9b3;
}
body.dark-mode .dropdown-menu {
  border-top: 2px solid #3a3b3d; /* 夜间模式下的上边框颜色 */
}
</style>
