import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 替换为你的后端服务器地址
        changeOrigin: true,
        // pathRewrite: { '^/api': '' }, // 可选：重写路径
      },
      '/imgs': {
        target: 'http://localhost:5000', // 替换为你的后端服务器地址
        changeOrigin: true,
        // pathRewrite: { '.imgs': '/imgs' }, // 可选：重写路径
      },
    },
  },
})
