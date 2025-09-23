<template>
  <div class="home-page">
    <!-- 背景容器 -->
    <div class="welcome-container">
      <h1 class="welcome-title">欢迎来到影片排行榜网站</h1>
      <p class="welcome-description">这里为你提供最新的影片排行和演员信息，快来探索吧！</p>

      <!-- 已登录状态显示 -->
      <div v-if="userStore.isLoggedIn" class="user-info">
        <h2 class="welcome-user">欢迎回来，{{ userStore.username }}！</h2>
        <p class="user-role">角色：{{ userStore.isAdmin ? '管理员' : '普通用户' }}</p>
        <p class="access-info">您现在可以访问所有页面内容</p>
        <button class="logout-button" @click="handleLogout">退出登录</button>
      </div>

      <!-- 未登录状态显示 -->
      <div v-else class="guest-info">
        <h2 class="guest-title">请先登录</h2>
        <p class="guest-description">登录后即可访问影片排行、演员信息等精彩内容</p>
        <button class="login-redirect-button" @click="goToLogin">立即登录</button>
      </div>

      <div class="welcome-buttons">
        <button class="welcome-button" @click="goToMovies">查看影片排行</button>
        <button class="welcome-button" @click="goToActors">查看演员列表</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../store/user.js'

export default {
  name: 'HomePage',
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  mounted() {
    // 页面加载时恢复登录状态
    this.userStore.restoreLoginState()
  },
  methods: {
    handleLogout() {
      this.userStore.logout()
    },

    goToLogin() {
      this.$router.push('/login') // 跳转到登录页面
    },

    goToMovies() {
      this.$router.push('/movies') // 跳转到影片排行榜页面
    },
    goToActors() {
      this.$router.push('/actors') // 跳转到演员列表页面
    },
  },
}
</script>

<style scoped>
.home-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 占满整个屏幕高度 */
  background: url('/background.jpg') no-repeat center center/cover; /* 背景图片 */
  text-align: center;
  color: white;
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

body.dark-mode .home-page {
  color: #a9a9b3;
}

body.dark-mode .welcome-button {
  background-color: #3a3a3a; /* 夜间模式按钮颜色 */
  color: #a9a9b3;
}

/* 访客信息样式 */
.guest-info {
  margin: 30px 0;
  padding: 20px;
  background-color: rgba(255, 193, 7, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 193, 7, 0.3);
  text-align: center;
}

.guest-title {
  font-size: 24px;
  margin-bottom: 10px;
  color: #ffc107;
}

.guest-description {
  font-size: 16px;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, 0.8);
}

.login-redirect-button {
  padding: 12px 24px;
  background-color: #ffc107;
  color: #333;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-redirect-button:hover {
  background-color: #ffb300;
}

/* 用户信息样式 */
.user-info {
  margin: 30px 0;
  padding: 20px;
  background-color: rgba(66, 185, 131, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(66, 185, 131, 0.3);
  text-align: center;
}

.welcome-user {
  font-size: 24px;
  margin-bottom: 10px;
  color: #42b983;
}

.user-role {
  font-size: 16px;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.8);
}

.access-info {
  font-size: 14px;
  margin-bottom: 15px;
  color: rgba(66, 185, 131, 0.8);
  font-style: italic;
}

.logout-button {
  padding: 8px 16px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #ff5252;
}

/* 夜间模式样式 */
body.dark-mode .guest-info {
  background-color: rgba(255, 193, 7, 0.15);
  border-color: rgba(255, 193, 7, 0.4);
}

body.dark-mode .guest-title {
  color: #ffc107;
}

body.dark-mode .guest-description {
  color: rgba(169, 169, 179, 0.8);
}

body.dark-mode .login-redirect-button {
  background-color: #ffc107;
  color: #333;
}

body.dark-mode .login-redirect-button:hover {
  background-color: #ffb300;
}

body.dark-mode .user-info {
  background-color: rgba(58, 58, 58, 0.3);
  border-color: rgba(58, 58, 58, 0.5);
}

body.dark-mode .welcome-user {
  color: #a9a9b3;
}

body.dark-mode .user-role {
  color: rgba(169, 169, 179, 0.8);
}

body.dark-mode .access-info {
  color: rgba(169, 169, 179, 0.6);
}
</style>
