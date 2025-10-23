<template>
  <div class="actors-container">
    <!-- 演员视图 -->
    <div class="actor-view">
      <!-- 顶部操作栏 -->
      <div class="view-header">
        <h1>演员列表</h1>

        <!-- 视图切换按钮 -->
        <div class="view-toggle">
          <button
            @click="currentView = 'favorite'"
            :class="{ active: currentView === 'favorite' }"
            class="view-btn"
            title="喜爱度视图"
          >
            <span class="material-icons">favorite</span>
          </button>
          <button
            @click="currentView = 'grid'"
            :class="{ active: currentView === 'grid' }"
            class="view-btn"
            title="网格视图"
          >
            <span class="material-icons">grid_view</span>
          </button>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索演员姓名..."
          class="search-input"
        />
      </div>

      <!-- 网格视图 -->
      <div v-if="currentView === 'grid'">
        <!-- 加载状态 -->
        <div v-if="!isDataLoaded" class="loading">
          <span class="material-icons">hourglass_empty</span>
          <p>正在加载演员数据...</p>
        </div>

        <!-- 搜索无结果提示 -->
        <div v-else-if="searchQuery.trim() && !hasSearchResults" class="no-results">
          <span class="material-icons">search_off</span>
          <p>未找到匹配"{{ searchQuery }}"的演员</p>
        </div>

        <!-- 演员网格 -->
        <div v-else class="actor-grid">
          <div v-for="actor in filteredActors" :key="actor.name" class="actor-item">
            <img
              :src="actor.cover"
              alt="演员封面"
              class="actor-cover"
              @click="goToActor(actor.name)"
              @error="setDefaultCover($event)"
            />
            <span class="actor-name">{{ actor.name }}</span>
          </div>
        </div>
      </div>

      <!-- 喜爱度视图 -->
      <div v-if="currentView === 'favorite'" class="favorite-view">
        <!-- 加载状态 -->
        <div v-if="!isDataLoaded" class="loading">
          <span class="material-icons">hourglass_empty</span>
          <p>正在加载演员数据...</p>
        </div>

        <!-- 搜索无结果提示 -->
        <div v-else-if="searchQuery.trim() && !hasSearchResults" class="no-results">
          <span class="material-icons">search_off</span>
          <p>未找到匹配"{{ searchQuery }}"的演员</p>
        </div>

        <!-- 喜爱度等级区域 -->
        <div v-for="level in favoriteLevels" :key="level" class="favorite-level">
          <div class="level-header">
            <h3>
              <span class="favorite-level-indicator">
                <span
                  v-for="i in 5"
                  :key="i"
                  class="level-heart"
                  :class="{ filled: i <= level, empty: i > level }"
                >
                  <span class="material-icons">
                    {{ i <= level ? 'favorite' : 'favorite_border' }}
                  </span>
                </span>
              </span>
            </h3>
            <button
              @click="toggleLevel(level)"
              class="collapse-btn"
              :class="{ collapsed: collapsedLevels.includes(level) }"
            >
              <span class="material-icons">
                {{ collapsedLevels.includes(level) ? 'expand_more' : 'expand_less' }}
              </span>
            </button>
          </div>
          <div class="level-actors" v-show="!collapsedLevels.includes(level)">
            <div v-for="actor in actorsByFavorite[level]" :key="actor.name" class="actor-item">
              <img
                :src="actor.cover"
                alt="演员封面"
                class="actor-cover"
                @click="goToActor(actor.name)"
                @error="setDefaultCover($event)"
              />
              <div class="actor-name-container">
                <span class="actor-name">{{ actor.name }}</span>
                <!-- 悬浮的喜爱度调整控件 -->
                <div class="favorite-controls">
                  <div class="favorite-display">
                    <span
                      v-for="i in 5"
                      :key="i"
                      class="mini-heart"
                      :class="{ filled: i <= actor.favorite, empty: i > actor.favorite }"
                      @click.stop="updateActorFavorite(actor.name, i)"
                    >
                      <span class="material-icons">
                        {{ i <= actor.favorite ? 'favorite' : 'favorite_border' }}
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ActorsPage',
  data() {
    return {
      actors: [],
      searchQuery: '', // 搜索查询
      currentView: 'favorite', // 当前视图模式：grid 或 favorite
      collapsedLevels: [], // 存储折叠的喜爱度等级
      defaultCover: '/imgs/default_cover.jpg', // 默认封面图片路径
    }
  },
  computed: {
    // 根据搜索查询过滤演员列表
    filteredActors() {
      if (!this.searchQuery.trim()) {
        return this.actors
      }
      return this.actors.filter((actor) =>
        actor.name.toLowerCase().includes(this.searchQuery.toLowerCase()),
      )
    },
    // 检查是否有搜索结果
    hasSearchResults() {
      return this.filteredActors.length > 0
    },
    // 检查数据是否已加载
    isDataLoaded() {
      return this.actors.length > 0
    },
    // 按喜爱度分组的演员数据
    actorsByFavorite() {
      const result = {}
      for (let i = 1; i <= 5; i++) {
        const actorsToFilter = this.searchQuery.trim() ? this.filteredActors : this.actors
        const filteredActors = actorsToFilter.filter((actor) => actor.favorite === i)
        result[i] = filteredActors.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'))
      }
      return result
    },
    // 获取有演员的喜爱度等级（用于v-for）
    favoriteLevels() {
      if (!this.isDataLoaded) return []
      const levels = []
      for (let i = 5; i >= 1; i--) {
        // 从高到低排序
        if (this.actorsByFavorite[i].length > 0) {
          levels.push(i)
        }
      }
      return levels
    },
  },
  methods: {
    goToActor(name) {
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
    },
    setDefaultCover(event) {
      event.target.src = this.defaultCover // 设置默认封面图片
    },
    async fetchActors() {
      try {
        const response = await axios.get('/api/actors')
        this.actors = response.data
      } catch (error) {
        console.error('Error fetching actors:', error)
      }
    },

    toggleLevel(level) {
      const index = this.collapsedLevels.indexOf(level)
      if (index > -1) {
        // 如果已折叠,则展开
        this.collapsedLevels.splice(index, 1)
      } else {
        // 如果已展开，则折叠
        this.collapsedLevels.push(level)
      }
    },
    // 搜索时自动展开包含结果的等级
    autoExpandSearchResults() {
      if (this.searchQuery.trim() && this.currentView === 'favorite') {
        // 清空折叠状态
        this.collapsedLevels = []
        // 只折叠没有搜索结果的等级
        for (let i = 1; i <= 5; i++) {
          if (this.actorsByFavorite[i].length === 0) {
            this.collapsedLevels.push(i)
          }
        }
      } else if (!this.searchQuery.trim() && this.currentView === 'favorite') {
        // 当没有搜索查询时，清空折叠状态，显示所有等级
        this.collapsedLevels = []
      }
    },
    // 更新演员喜爱度
    async updateActorFavorite(actorName, newFavorite) {
      try {
        const response = await axios.put(`/api/update-actor-favorite/${actorName}`, {
          favorite: newFavorite,
        })
        if (response.data.success) {
          // 更新本地数据
          const actor = this.actors.find((a) => a.name === actorName)
          if (actor) {
            actor.favorite = newFavorite
          }
          this.$message.success('喜爱度更新成功！')
        } else {
          this.$message.error('更新失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error updating favorite:', error)
        this.$message.error('更新失败，请稍后再试！')
      }
    },
  },
  watch: {
    // 监听搜索查询变化
    searchQuery() {
      this.autoExpandSearchResults()
    },
    // 监听视图切换
    currentView() {
      if (this.currentView === 'favorite') {
        // 切换到favorite视图时，清空折叠状态
        this.collapsedLevels = []
      }
    },
  },
  async mounted() {
    await this.fetchActors()
    // 确保在数据加载后正确初始化favorite视图
    if (this.currentView === 'favorite') {
      this.autoExpandSearchResults()
    }

    // 监听演员创建事件
    this.$eventBus.on('actor-created', () => {
      this.fetchActors()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('actor-created')
  },
}
</script>

<style scoped>
.actor-view {
  max-width: 1200px;
  justify-content: center; /* 水平居中 */
  margin: auto;
}

/* 视图头部样式 */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 20px;
}

.view-toggle {
  display: flex;
  gap: 10px;
}

.view-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  background: var(--bg-primary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  color: var(--primary-color);
}

.view-btn:hover {
  border-color: var(--primary-color);
  background: var(--bg-gradient-light);
}

.view-btn.active {
  border-color: var(--primary-color);
  background: var(--primary-gradient);
  color: white;
}

.view-btn .material-icons {
  font-size: 18px;
}

/* 搜索容器样式 */
.search-container {
  margin: 20px 10px;
  text-align: center;
}

.search-input {
  width: 80%;
  max-width: 400px;
  padding: 12px 16px;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--bg-gradient-light);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.actor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 40px;
  margin-top: 20px;
}

.actor-item {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 居中对齐 */
  text-align: center;
  padding: 10px;
  border: 2px solid var(--border-light);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  background: var(--card-bg);
  /* 不设置固定高度，让内容决定高度 */
}

.actor-item:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.actor-cover {
  max-width: 200px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 10%; /* 圆形封面 */
  cursor: pointer;
  transition: transform 0.2s ease;
}

.actor-cover:hover {
  transform: scale(1.05);
}

.actor-name-container {
  position: relative;
  display: inline-block;
  margin-top: 10px;
}

.actor-name {
  font-size: 16px;
  font-weight: bold;
  word-wrap: break-word; /* 长名字自动换行 */
  cursor: pointer;
  transition: color 0.2s ease;
}

.actor-name:hover {
  color: var(--primary-color);
}

/* 悬浮的喜爱度控件 */
.favorite-controls {
  position: absolute;
  top: -55px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 4px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.favorite-controls::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: rgba(0, 0, 0, 0.9);
}

.actor-name-container:hover .favorite-controls {
  opacity: 1;
  visibility: visible;
}

.favorite-display {
  display: flex;
  align-items: center;
  gap: 2px;
}

.mini-heart {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 3px;
  border-radius: 4px;
  min-width: 24px;
  min-height: 24px;
  justify-content: center;
}

.mini-heart:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.15);
}

.mini-heart .material-icons {
  font-size: 18px;
  transition: all 0.2s ease;
}

.mini-heart.filled .material-icons {
  color: #e91e63;
}

.mini-heart.empty .material-icons {
  color: rgba(255, 255, 255, 0.7);
}

.mini-heart:hover .material-icons {
  color: #e91e63;
}

/* 喜爱度视图样式 */
.favorite-view {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.loading,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: var(--bg-gradient-light);
  border-radius: 12px;
  border: 2px dashed var(--border-medium);
  color: var(--primary-color);
}

.loading .material-icons {
  font-size: 48px;
  margin-bottom: 16px;
  color: var(--primary-color);
  animation: spin 2s linear infinite;
}

.no-results .material-icons {
  font-size: 48px;
  margin-bottom: 16px;
  color: var(--secondary-color);
}

.loading p,
.no-results p {
  margin: 0;
  font-size: 16px;
  text-align: center;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.favorite-level {
  border: 2px solid var(--border-light);
  border-radius: 12px;
  padding: 20px;
  background: var(--bg-gradient-light);
  box-shadow: var(--shadow-sm);
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--border-light);
  flex-wrap: nowrap;
  gap: 10px;
}

.level-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: var(--primary-color);
  font-size: 18px;
  flex-shrink: 0;
  font-weight: 600;
}

.favorite-level-indicator {
  display: flex;
  align-items: center;
  gap: 2px;
}

.level-heart {
  display: flex;
  align-items: center;
}

.level-heart .material-icons {
  font-size: 20px;
  transition: all 0.2s ease;
}

.level-heart.filled .material-icons {
  color: #e91e63; /* 粉色爱心 */
}

.level-heart.empty .material-icons {
  color: #ddd; /* 灰色爱心 */
}

.collapse-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-btn:hover {
  background: var(--bg-gradient-medium);
  transform: scale(1.1);
}

.collapse-btn .material-icons {
  color: var(--primary-color);
  font-size: 20px;
  transition: transform 0.3s ease;
}

.collapse-btn.collapsed .material-icons {
  transform: rotate(180deg);
}

.level-actors {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  transition: all 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    align-items: stretch;
  }

  .view-toggle {
    justify-content: center;
  }

  .level-header {
    gap: 8px;
  }

  .level-header h3 {
    font-size: 16px;
  }

  .level-actors {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  /* 移动端爱心控件优化 */
  .mini-heart {
    min-width: 28px;
    min-height: 28px;
    padding: 4px;
  }

  .mini-heart .material-icons {
    font-size: 20px;
  }

  .favorite-controls {
    top: -65px;
    padding: 12px 18px;
    gap: 6px;
  }
}

@media (max-width: 480px) {
  .mini-heart {
    min-width: 32px;
    min-height: 32px;
    padding: 5px;
  }

  .mini-heart .material-icons {
    font-size: 22px;
  }

  .favorite-controls {
    top: -70px;
    padding: 14px 20px;
    gap: 8px;
  }

  .level-header {
    gap: 6px;
  }

  .level-header h3 {
    font-size: 14px;
  }

  .favorite-level-indicator {
    gap: 1px;
  }

  .level-heart .material-icons {
    font-size: 16px;
  }
}
</style>
