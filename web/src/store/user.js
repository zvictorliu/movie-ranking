import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    user: null,
    token: null,
  }),

  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    username: (state) => state.user?.username || '',
  },

  actions: {
    async login(credentials) {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(credentials),
        })

        const data = await response.json()

        if (data.success) {
          this.isLoggedIn = true
          this.user = data.user
          // 将用户信息保存到localStorage
          localStorage.setItem('user', JSON.stringify(data.user))
          localStorage.setItem('isLoggedIn', 'true')
          return { success: true, message: data.message }
        } else {
          return { success: false, message: data.message }
        }
      } catch (error) {
        console.error('登录错误:', error)
        return { success: false, message: '网络错误，请稍后重试' }
      }
    },

    logout() {
      this.isLoggedIn = false
      this.user = null
      this.token = null
      // 清除localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('isLoggedIn')
    },

    // 从localStorage恢复登录状态
    restoreLoginState() {
      const savedUser = localStorage.getItem('user')
      const savedLoginState = localStorage.getItem('isLoggedIn')

      if (savedUser && savedLoginState === 'true') {
        try {
          this.user = JSON.parse(savedUser)
          this.isLoggedIn = true
        } catch (error) {
          console.error('恢复登录状态失败:', error)
          this.logout()
        }
      }
    },
  },
})
