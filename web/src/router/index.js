import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user.js'
import HomePage from '../views/HomePage.vue' // 引入主页组件
import LoginPage from '../views/LoginPage.vue' // 引入登录页面组件
import MovieDetailPage from '../views/MovieDetail.vue' // 引入影片详情页组件
import ActorDetailPage from '../views/ActorDetail.vue' // 引入演员详情页组件
import ActorsPage from '../views/ActorsPage.vue' // 引入演员页面
import MoviesPage from '../views/MoviesPage.vue' // 引入影片页面
import TagsPage from '../views/TagsPage.vue' // 引入标签页面
import TagDetail from '../views/TagDetail.vue' // 引入标签详情页面
import PostsPage from '../views/PostsPage.vue' // 引入博客列表页面
import PostsDetail from '../views/PostsDetail.vue' // 引入博客详情页面
import ImgbedPage from '../views/ImgbedPage.vue' // 引入图床页面

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
    meta: { requiresAuth: false }, // 首页不需要认证
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    meta: { requiresAuth: false }, // 登录页面不需要认证
  },
  {
    path: '/movies',
    name: 'MoviesPage',
    component: MoviesPage,
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/actors',
    name: 'ActorsPage',
    component: ActorsPage,
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/tags',
    name: 'TagsPage',
    component: TagsPage,
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: MovieDetailPage,
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/actor/:name',
    name: 'ActorDetail',
    component: ActorDetailPage,
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/tags/:tagName', // 动态路由参数
    name: 'TagDetail',
    component: TagDetail, // 标签详情页面路由
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/posts',
    name: 'PostsPage',
    component: PostsPage, // 博客列表页面路由
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/posts/:slug',
    name: 'PostsDetail',
    component: PostsDetail, // 博客详情页面路由
    meta: { requiresAuth: true }, // 需要认证
  },
  {
    path: '/imgbed',
    name: 'ImgbedPage',
    component: ImgbedPage, // 图床页面路由
    meta: { requiresAuth: true }, // 需要认证
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 恢复登录状态（如果还没有恢复的话）
  if (!userStore.isLoggedIn) {
    userStore.restoreLoginState()
  }

  // 检查路由是否需要认证
  if (to.meta.requiresAuth) {
    if (userStore.isLoggedIn) {
      // 已登录，允许访问
      next()
    } else {
      // 未登录，重定向到登录页面
      next({
        path: '/login',
        query: {
          redirect: to.fullPath,
          message: '请先登录后再访问该页面',
        },
      })
    }
  } else {
    // 不需要认证的路由，直接访问
    next()
  }
})

export default router
