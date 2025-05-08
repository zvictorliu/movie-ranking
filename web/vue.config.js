const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // devServer: {
  //   proxy: {
  //     '/imgs': {
  //       target: 'http://localhost:5000', // 后端服务地址
  //       changeOrigin: true,
  //       pathRewrite: {
  //         '^/imgs': '/imgs', // 重写路径
  //       },
  //     },
  //   },
  // },

})
