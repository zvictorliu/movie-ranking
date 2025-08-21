import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue' // 引入主页组件
import MovieDetailPage from '../views/MovieDetail.vue' // 引入影片详情页组件
import ActorDetailPage from '../views/ActorDetail.vue' // 引入演员详情页组件
import ActorsPage from '../views/ActorsPage.vue' // 引入演员页面
import MoviesPage from '../views/MoviesPage.vue' // 引入影片页面
import TagsPage from '../views/TagsPage.vue' // 引入标签页面
import TagDetail from '../views/TagDetail.vue' // 引入标签详情页面
import PostsPage from '../views/PostsPage.vue' // 引入博客列表页面
import PostsDetail from '../views/PostsDetail.vue' // 引入博客详情页面

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/movies',
    name: 'MoviesPage',
    component: MoviesPage,
  },
  {
    path: '/actors',
    name: 'ActorsPage',
    component: ActorsPage,
  },
  {
    path: '/tags',
    name: 'TagsPage',
    component: TagsPage,
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: MovieDetailPage,
  },
  {
    path: '/actor/:name',
    name: 'ActorDetail',
    component: ActorDetailPage,
  },
  {
    path: '/tags/:tagName', // 动态路由参数
    name: 'TagDetail',
    component: TagDetail, // 标签详情页面路由
  },
  {
    path: '/posts',
    name: 'PostsPage',
    component: PostsPage, // 博客列表页面路由
  },
  {
    path: '/posts/:slug',
    name: 'PostsDetail',
    component: PostsDetail, // 博客详情页面路由
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
