<template>
  <div class="home-page">
    <!-- 动态背景 -->
    <div class="background-animation">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- 主要内容 -->
    <div class="content-wrapper">
      <!-- Hero 区域 -->
      <div class="hero-section">
        <div class="hero-icon">
          <span class="material-icons">movie</span>
        </div>
        <h1 class="hero-title">影片排行榜</h1>
        <p class="hero-subtitle">铭记美丽的瞬间</p>
      </div>

      <!-- 状态卡片 -->
      <div class="status-card">
        <div v-if="userStore.isLoggedIn" class="user-section">
          <div class="user-avatar">
            <span class="material-icons">account_circle</span>
          </div>
          <div class="user-details">
            <h2 class="user-name">{{ userStore.username }}</h2>
            <p class="user-role">
              <span class="role-badge" :class="userStore.isAdmin ? 'admin' : 'user'">
                {{ userStore.isAdmin ? '管理员' : '用户' }}
              </span>
            </p>
          </div>
          <button class="logout-btn" @click="handleLogout" title="退出登录">
            <span class="material-icons">logout</span>
          </button>
        </div>

        <div v-else class="guest-section">
          <div class="guest-icon">
            <span class="material-icons">lock</span>
          </div>
          <h2 class="guest-title">请先登录</h2>
          <p class="guest-description">登录后即可访问影片排行、演员信息等精彩内容</p>
          <button class="login-btn" @click="goToLogin">
            <span class="material-icons">login</span>
            立即登录
          </button>
        </div>
      </div>

      <!-- 快捷入口 -->
      <div class="quick-access">
        <h3 class="section-title">快捷入口</h3>
        <div class="access-grid">
          <div class="access-card" @click="goToMovies">
            <div class="card-icon movies">
              <span class="material-icons">movie</span>
            </div>
            <h4 class="card-title">影片排行</h4>
            <p class="card-description">查看和管理影片评分</p>
          </div>

          <div class="access-card" @click="goToActors">
            <div class="card-icon actors">
              <span class="material-icons">people</span>
            </div>
            <h4 class="card-title">演员列表</h4>
            <p class="card-description">浏览演员信息资料</p>
          </div>

          <div class="access-card" @click="goToTags">
            <div class="card-icon tags">
              <span class="material-icons">local_offer</span>
            </div>
            <h4 class="card-title">标签分类</h4>
            <p class="card-description">按标签筛选影片</p>
          </div>

          <div class="access-card" @click="goToPosts">
            <div class="card-icon posts">
              <span class="material-icons">article</span>
            </div>
            <h4 class="card-title">博客文章</h4>
            <p class="card-description">阅读影评和随笔</p>
          </div>
        </div>
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
    this.userStore.restoreLoginState()
  },
  methods: {
    handleLogout() {
      this.userStore.logout()
      this.$message.success('已退出登录')
    },
    goToLogin() {
      this.$router.push('/login')
    },
    goToMovies() {
      this.$router.push('/movies')
    },
    goToActors() {
      this.$router.push('/actors')
    },
    goToTags() {
      this.$router.push('/tags')
    },
    goToPosts() {
      this.$router.push('/posts')
    },
  },
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  background: var(--primary-gradient);
}

/* 动态背景 */
.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.5;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: var(--primary-gradient);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  bottom: -50px;
  right: -50px;
  animation-delay: 7s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 14s;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

/* 内容区域 */
.content-wrapper {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

/* Hero 区域 */
.hero-section {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.8s ease-out;
}

.hero-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.hero-icon .material-icons {
  font-size: 48px;
  color: white;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 300;
}

/* 状态卡片 */
.status-card {
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: var(--shadow-md);
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  background: var(--primary-gradient);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar .material-icons {
  font-size: 36px;
  color: white;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 5px;
}

.user-role {
  margin: 0;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
}

.role-badge.admin {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.role-badge.user {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.logout-btn {
  width: 44px;
  height: 44px;
  background: #ff6b6b;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.logout-btn .material-icons {
  font-size: 20px;
  color: white;
}

.logout-btn:hover {
  background: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
}

/* 访客区域 */
.guest-section {
  text-align: center;
}

.guest-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.guest-icon .material-icons {
  font-size: 32px;
  color: white;
}

.guest-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.guest-description {
  font-size: 16px;
  color: var(--text-tertiary);
  margin-bottom: 20px;
}

.login-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: var(--primary-gradient);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.login-btn .material-icons {
  font-size: 20px;
}

/* 快捷入口 */
.quick-access {
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.access-card {
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  text-align: center;
}

.access-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.card-icon .material-icons {
  font-size: 32px;
  color: white;
}

.card-icon.movies {
  background: var(--primary-gradient);
}

.card-icon.actors {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.tags {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.posts {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.access-card:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.card-description {
  font-size: 14px;
  color: var(--text-tertiary);
  line-height: 1.5;
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-page {
    background: var(--primary-gradient);
  }

  .gradient-orb {
    display: none; /* 移动端隐藏动态背景以提升性能 */
  }

  .content-wrapper {
    padding: 30px 15px;
  }

  .hero-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    margin-bottom: 15px;
  }

  .hero-icon .material-icons {
    font-size: 36px;
  }

  .hero-title {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .hero-subtitle {
    font-size: 14px;
    line-height: 1.5;
  }

  .hero-section {
    margin-bottom: 30px;
  }

  .status-card {
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 30px;
  }

  .user-section {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .user-avatar {
    width: 56px;
    height: 56px;
  }

  .user-avatar .material-icons {
    font-size: 32px;
  }

  .user-name {
    font-size: 20px;
  }

  .logout-btn {
    width: 100%;
    height: 40px;
    border-radius: 10px;
  }

  .guest-icon {
    width: 56px;
    height: 56px;
    margin-bottom: 12px;
  }

  .guest-icon .material-icons {
    font-size: 28px;
  }

  .guest-title {
    font-size: 20px;
  }

  .guest-description {
    font-size: 14px;
    line-height: 1.5;
  }

  .login-btn {
    width: 100%;
    padding: 12px 24px;
    border-radius: 10px;
  }

  .section-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .access-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 30px;
  }

  .access-card {
    padding: 20px 15px;
    border-radius: 12px;
  }

  .access-card:hover {
    transform: translateY(-4px);
  }

  .card-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    margin-bottom: 10px;
  }

  .card-icon .material-icons {
    font-size: 24px;
  }

  .card-title {
    font-size: 16px;
    margin-bottom: 5px;
  }

  .card-description {
    font-size: 12px;
    line-height: 1.4;
  }

  .footer {
    margin-top: 20px;
  }

  .footer-text {
    font-size: 14px;
  }

  .footer-text .material-icons {
    font-size: 16px;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .content-wrapper {
    padding: 20px 12px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-subtitle {
    font-size: 13px;
  }

  .access-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .access-card {
    padding: 20px;
  }

  .card-icon {
    width: 52px;
    height: 52px;
  }

  .card-icon .material-icons {
    font-size: 28px;
  }

  .card-title {
    font-size: 17px;
  }

  .card-description {
    font-size: 13px;
  }
}

</style>
