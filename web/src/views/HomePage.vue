<template>
  <div class="home-page">
    <ThreeCylinderScene
      v-if="projects.length"
      :projects="projects"
      :spiral="isSpiral"
      @open-project="onOpen"
    />

    <div v-else class="home-page__loading">
      <p>{{ error || '正在加载影片封面…' }}</p>
    </div>

    <header class="home-page__chrome">
      <div class="chrome-brand">
        <span class="material-icons chrome-brand__icon">movie</span>
        <span class="chrome-brand__text">影片排行榜</span>
      </div>

      <div class="layout-switch" :class="{ 'is-spiral': isSpiral }">
        <span class="layout-switch__pill" aria-hidden="true"></span>
        <button
          type="button"
          class="layout-switch__btn"
          :class="{ 'is-active': !isSpiral }"
          @click="isSpiral = false"
        >
          Rings
        </button>
        <button
          type="button"
          class="layout-switch__btn"
          :class="{ 'is-active': isSpiral }"
          @click="isSpiral = true"
        >
          Spiral
        </button>
      </div>

      <div class="chrome-actions">
        <button type="button" class="chrome-btn" @click="goToMovies" title="影片排行">
          <span class="material-icons">movie</span>
        </button>
        <button type="button" class="chrome-btn" @click="handleLogout" title="退出登录">
          <span class="material-icons">logout</span>
        </button>
      </div>
    </header>

    <footer class="home-footer">
      <span class="home-footer__item home-footer__left">
        <span class="home-footer__line">铭记美丽的瞬间</span>
      </span>
      <span class="home-footer__item home-footer__center">
        <span class="home-footer__line">
          <button type="button" class="home-footer__link" @click="goToMovies">
            影片 {{ movieCount }}
          </button>
          <span class="home-footer__sep">/</span>
          <button type="button" class="home-footer__link" @click="goToActors">
            演员 {{ actorCount }}
          </button>
        </span>
      </span>
      <span class="home-footer__item home-footer__right">
        <span class="home-footer__line">© {{ currentYear }}</span>
      </span>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useUserStore } from '../store/user.js'
import ThreeCylinderScene from '../components/three/ThreeCylinderScene.vue'
import { movieCover } from '../utils/cover.js'

const GALLERY_SIZE = 10

function pickRandomMovies(movies, count) {
  const pool = [...movies]
  for (let i = pool.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[pool[i], pool[j]] = [pool[j], pool[i]]
  }
  return pool.slice(0, Math.min(count, pool.length))
}

const router = useRouter()
const userStore = useUserStore()
const projects = ref([])
const isSpiral = ref(false)
const error = ref('')
const movieCount = ref(0)
const actorCount = ref(0)
const currentYear = new Date().getFullYear()

function goToMovies() {
  router.push({ name: 'MoviesPage' })
}

function goToActors() {
  router.push({ name: 'ActorsPage' })
}

function handleLogout() {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push({ path: '/login', query: { redirect: '/' } })
}

function onOpen(project) {
  const id = project?.id
  if (!id || typeof id !== 'string') return
  router.push({ name: 'MovieDetail', params: { id } })
}

onMounted(async () => {
  userStore.restoreLoginState()

  const moviesReq = axios.get('/api/movies').catch((err) => {
    console.error('[HomePage] Failed to load movies', err)
    return null
  })
  const actorsReq = axios.get('/api/actors').catch((err) => {
    console.error('[HomePage] Failed to load actors', err)
    return null
  })

  const [moviesRes, actorsRes] = await Promise.all([moviesReq, actorsReq])

  actorCount.value = Array.isArray(actorsRes?.data) ? actorsRes.data.length : 0

  if (!moviesRes) {
    error.value = '无法加载影片列表，请确认后端服务已启动'
    projects.value = []
    return
  }

  const list = (moviesRes.data || [])
    .filter((m) => m.cover)
    .map((m) => ({
      id: m.id,
      title: m.title,
      cover: movieCover(m, 'small'),
      image: movieCover(m, 'original'),
      rating: m.rating,
    }))

  movieCount.value = list.length

  if (!list.length) {
    error.value = '暂无可用影片封面'
    projects.value = []
    return
  }

  projects.value = pickRandomMovies(list, GALLERY_SIZE)
})
</script>

<style scoped>
.home-page {
  position: fixed;
  inset: 0;
  z-index: 1;
  background: #f3f5fa;
}

.home-page__loading {
  display: grid;
  place-items: center;
  height: 100%;
  color: #5a647c;
  font-size: 15px;
}

.home-page__chrome {
  position: absolute;
  inset: 0 0 auto;
  z-index: 2;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  pointer-events: none;
}

.chrome-brand,
.layout-switch,
.layout-switch__btn,
.chrome-actions,
.chrome-btn {
  pointer-events: auto;
}

.chrome-brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #1a1f36;
}

.chrome-brand__icon {
  font-size: 28px;
  opacity: 0.9;
  color: #1500e1;
}

.chrome-brand__text {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.layout-switch {
  position: relative;
  justify-self: center;
  display: inline-grid;
  grid-template-columns: 1fr 1fr;
  width: 180px;
  height: 36px;
  padding: 3px;
  border-radius: 999px;
  background: rgba(26, 31, 54, 0.06);
  border: 1px solid rgba(26, 31, 54, 0.08);
  backdrop-filter: blur(10px);
}

.layout-switch__pill {
  position: absolute;
  top: 3px;
  left: 3px;
  width: calc(50% - 3px);
  height: calc(100% - 6px);
  border-radius: 999px;
  background: #1500e1;
  transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

.layout-switch.is-spiral .layout-switch__pill {
  transform: translateX(100%);
}

.layout-switch__btn {
  position: relative;
  z-index: 1;
  border: 0;
  background: transparent;
  color: rgba(26, 31, 54, 0.55);
  font-size: 13px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
}

.layout-switch__btn.is-active {
  color: #fff;
}

.chrome-actions {
  justify-self: end;
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.chrome-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid rgba(26, 31, 54, 0.08);
  border-radius: 50%;
  background: rgba(26, 31, 54, 0.06);
  color: #1a1f36;
  cursor: pointer;
  backdrop-filter: blur(8px);
}

.chrome-btn:hover {
  background: rgba(26, 31, 54, 0.1);
}

.home-footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 16px;
  padding: 22px 28px 26px;
  pointer-events: none;
}

.home-footer__item {
  display: inline-flex;
  align-items: center;
  min-width: 0;
}

.home-footer__left {
  justify-content: flex-start;
}

.home-footer__center {
  justify-content: center;
}

.home-footer__right {
  justify-content: flex-end;
}

.home-footer__line {
  color: rgba(26, 31, 54, 0.55);
  font-size: 12px;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.home-footer__sep {
  margin: 0 10px;
  color: rgba(26, 31, 54, 0.28);
}

.home-footer__link {
  pointer-events: auto;
  border: 0;
  padding: 0;
  background: transparent;
  color: rgba(26, 31, 54, 0.7);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
}

.home-footer__link:hover {
  color: #1500e1;
}

@media (max-width: 720px) {
  .home-page__chrome {
    grid-template-columns: 1fr auto;
    grid-template-areas:
      'brand actions'
      'switch switch';
    row-gap: 12px;
  }

  .chrome-brand {
    grid-area: brand;
  }

  .chrome-actions {
    grid-area: actions;
  }

  .layout-switch {
    grid-area: switch;
  }

  .chrome-brand__text {
    font-size: 16px;
  }

  .home-footer {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 8px;
    padding: 16px 20px 20px;
    text-align: center;
  }

  .home-footer__left,
  .home-footer__center,
  .home-footer__right {
    justify-content: center;
  }

  .home-footer__left {
    order: 2;
  }

  .home-footer__center {
    order: 1;
  }

  .home-footer__right {
    order: 3;
  }
}
</style>
