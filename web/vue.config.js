const { defineConfig } = require('@vue/cli-service')
module.exports = {
  devServer: {
    port: 8080, // Vue应用运行的端口
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 替换为你的后端服务器地址
        changeOrigin: true,},
        // pathRewrite: { '^/api': '' }, // 可选：重写路径
      '/imgs': {
        target: 'http://localhost:5000', // 替换为你的后端服务器地址
        changeOrigin: true,
        // pathRewrite: { '^/imgs': '../imgs' }, // 可选：重写路径
      },
    },
  },
}
