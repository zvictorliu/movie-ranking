<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1 class="login-title">用户登录</h1>
        <p class="login-subtitle">请登录以访问影片排行榜网站</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <input
            id="username"
            type="text"
            v-model="loginForm.username"
            placeholder="请输入用户名"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label for="password" class="form-label">密码</label>
          <input
            id="password"
            type="password"
            v-model="loginForm.password"
            placeholder="请输入密码"
            class="form-input"
            required
          />
        </div>

        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p v-if="loginError" class="error-message">{{ loginError }}</p>

      <!-- <div class="login-footer">
        <p class="demo-info">演示账号：</p>
        <p class="demo-account">管理员：admin / admin123</p>
        <p class="demo-account">普通用户：user / user123</p>
      </div> -->
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../store/user.js'

export default {
  name: 'LoginPage',
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
      },
      isLoading: false,
      loginError: '',
    }
  },
  mounted() {
    // 检查是否有重定向消息
    const redirectMessage = this.$route.query.message
    if (redirectMessage) {
      this.loginError = redirectMessage
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      this.loginError = ''

      try {
        const result = await this.userStore.login(this.loginForm)
        if (result.success) {
          // 登录成功，清空表单
          this.loginForm.username = ''
          this.loginForm.password = ''

          // 检查是否有重定向路径
          const redirectPath = this.$route.query.redirect
          if (redirectPath) {
            // 重定向到用户原本想访问的页面
            this.$router.push(redirectPath)
          } else {
            // 没有重定向路径，跳转到首页
            this.$router.push('/')
          }
        } else {
          this.loginError = result.message
        }
      } catch {
        this.loginError = '登录失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },
  },
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--primary-gradient);
  padding: 20px;
}

.login-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease;
  background-color: #fff;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--input-focus-shadow);
}

.form-input::placeholder {
  color: var(--text-muted);
}

.login-button {
  padding: 14px 24px;
  background: var(--btn-primary-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  margin-top: 10px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.login-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  text-align: center;
  margin-top: 15px;
  padding: 10px;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.login-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e1e5e9;
  text-align: center;
}

.demo-info {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
  font-weight: 500;
}

.demo-account {
  font-size: 12px;
  color: var(--text-muted);
  margin: 2px 0;
  font-family: monospace;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 30px 20px;
    margin: 10px;
  }

  .login-title {
    font-size: 24px;
  }
}
</style>
