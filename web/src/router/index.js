import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue'; // 引入主页组件
import MovieDetailPage from '../views/MovieDetail.vue'; // 引入影片详情页组件
import ActorDetailPage from '../views/ActorDetail.vue'; // 引入演员详情页组件

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;