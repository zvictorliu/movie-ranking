<template>
  <header class="app-header">
    <div class="logo" @click="goToHome">
      <img src="/home-button.png" alt="Logo" />
    </div>
    <h1 class="title">影片排行榜</h1>

    <button class="toggle-button" @click="toggleView" title="切换视图">
      <span class="material-icons">{{ viewStore.isMovieView ? "switch_video" : "theater_comedy" }}</span>
    </button>
  </header>
</template>

<script>
import { useViewStore } from '../store/view';
export default {
  name: 'Header',
  setup() {
    const viewStore = useViewStore();
    return { viewStore };
  },
  methods: {
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
    },
    toggleView() {
      this.viewStore.toggleView();
    },
  },
}
</script>

<style scoped>
.app-header {
  background-color: #f8f8f8;
  padding: 10px 20px;
  align-items: center;
  display: flex;
}

.logo img {
  width: 50px;
  cursor: pointer;
}

.title {
  color: black;
  font-size: 24px;
  margin: 0 10px;
}

.toggle-icon {
  font-size: 24px;
  cursor: pointer;
  margin-right: 10px;
  color: #999;
}
.toggle-icon.active {
  color: #42b983; /* 高亮当前选中的图标 */
}

.toggle-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-left: auto;
}
.toggle-button:hover {
  background-color: #33a07c;
}

.material-icons {
  font-size: 24px; /* 设置图标的大小 */
}
</style>
