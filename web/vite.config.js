import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

const backendUrl = process.env.VITE_BACKEND_URL || 'http://localhost:5000'

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
        target: backendUrl,
        changeOrigin: true,
        // pathRewrite: { '^/api': '' }, // 可选：重写路径
      },
      '/imgs': {
        target: backendUrl,
        changeOrigin: true,
        // pathRewrite: { '.imgs': '/imgs' }, // 可选：重写路径
      },
    },
  },
})
