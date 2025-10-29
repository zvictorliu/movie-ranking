<template>
  <div class="dashboard-page">
    <section class="dashboard-intro">
      <h1>数据总览</h1>
      <p>快速掌握影片站点的最新动态与核心指标</p>
    </section>

    <div v-if="loading" class="dashboard-state">
      <el-skeleton :rows="6" animated />
    </div>
    <div v-else-if="error" class="dashboard-state">
      <el-alert :title="error" type="error" show-icon />
    </div>
    <div v-else class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <span class="material-icons">movie</span>
          </div>
          <div class="stat-info">
            <span class="stat-label">影片数量</span>
            <span class="stat-value">{{ stats.movies }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <span class="material-icons">people</span>
          </div>
          <div class="stat-info">
            <span class="stat-label">演员数量</span>
            <span class="stat-value">{{ stats.actors }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <span class="material-icons">local_offer</span>
          </div>
          <div class="stat-info">
            <span class="stat-label">标签数量</span>
            <span class="stat-value">{{ stats.tags }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <span class="material-icons">article</span>
          </div>
          <div class="stat-info">
            <span class="stat-label">博客数量</span>
            <span class="stat-value">{{ stats.posts }}</span>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <section class="panel chart-panel">
          <header class="panel-header">
            <h2>影片评分分布</h2>
            <small>统计所有影片在各评分区间的数量</small>
          </header>
          <div class="chart-wrapper">
            <v-chart v-if="movieChartOption" :option="movieChartOption" autoresize class="pie-chart" />
            <el-empty v-else description="暂无影片评分数据" />
          </div>
        </section>

        <section class="panel chart-panel">
          <header class="panel-header">
            <h2>演员喜爱度分布</h2>
            <small>统计演员喜爱度（1-5）在各评分区间的数量</small>
          </header>
          <div class="chart-wrapper">
            <v-chart v-if="actorChartOption" :option="actorChartOption" autoresize class="pie-chart" />
            <el-empty v-else description="暂无演员喜爱度数据" />
          </div>
        </section>

        <section class="panel chart-panel">
          <header class="panel-header">
            <h2>标签使用分布</h2>
            <small>统计标签被使用的次数</small>
          </header>
          <div class="chart-wrapper">
            <v-chart
              v-if="tagChartOption"
              :option="tagChartOption"
              autoresize
              class="pie-chart"
              @click="handleTagChartClick"
            />
            <el-empty v-else description="暂无标签数据" />
          </div>
        </section>
      </div>

      <div class="panels">
        <section class="panel">
          <header class="panel-header">
            <h2>评分最高的影片</h2>
            <small>根据当前数据自动排序</small>
          </header>
          <ul class="panel-list" v-if="topMovies.length">
            <li v-for="movie in topMovies" :key="movie.id || movie.title" class="panel-item">
              <div class="item-title">{{ movie.title }}</div>
              <div class="item-meta">
                <span class="material-icons">star</span>
                <span>{{ formatRating(movie.rating) }}</span>
              </div>
            </li>
          </ul>
          <el-empty v-else description="暂无影片数据" />
        </section>

        <section class="panel">
          <header class="panel-header">
            <h2>最新博客</h2>
            <small>最近发布的三篇文章</small>
          </header>
          <ul class="panel-list" v-if="latestPosts.length">
            <li v-for="post in latestPosts" :key="post.slug || post.title" class="panel-item">
              <div class="item-title">{{ post.title }}</div>
              <div class="item-meta">
                <span class="material-icons">event</span>
                <span>{{ formatDate(post.date) }}</span>
              </div>
            </li>
          </ul>
          <el-empty v-else description="暂无博客数据" />
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { LegendComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, PieChart, LegendComponent, TooltipComponent, TitleComponent])

const RATING_BUCKETS = [
  { label: '1 分', min: 1, max: 1.5 },
  { label: '2 分', min: 1.5, max: 2.5 },
  { label: '3 分', min: 2.5, max: 3.5 },
  { label: '4 分', min: 3.5, max: 4.5 },
  { label: '5 分', min: 4.5, max: 5.01 }, // 包含 5 分
]

export default {
  name: 'DashboardPage',
  components: {
    VChart,
  },
  data() {
    return {
      loading: false,
      error: '',
      stats: {
        movies: 0,
        actors: 0,
        tags: 0,
        posts: 0,
      },
      topMovies: [],
      latestPosts: [],
      movieChartOption: null,
      actorChartOption: null,
      tagChartOption: null,
    }
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true
      this.error = ''
      try {
        const [moviesRes, actorsRes, tagsRes, postsRes] = await Promise.all([
          axios.get('/api/movies'),
          axios.get('/api/actors'),
          axios.get('/api/tags'),
          axios.get('/api/posts'),
        ])

        const movies = Array.isArray(moviesRes.data) ? moviesRes.data : []
        const actors = Array.isArray(actorsRes.data) ? actorsRes.data : []
        const tags = Array.isArray(tagsRes.data) ? tagsRes.data : []
        const posts = Array.isArray(postsRes.data?.posts) ? postsRes.data.posts : []

        this.stats = {
          movies: movies.length,
          actors: actors.length,
          tags: tags.length,
          posts: posts.length,
        }

        this.topMovies = [...movies]
          .filter((item) => typeof item.rating === 'number')
          .sort((a, b) => (b.rating || 0) - (a.rating || 0))
          .slice(0, 3)
        this.latestPosts = [...posts]
          .filter((item) => item.date)
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .slice(0, 3)

        this.movieChartOption = this.buildPieOption('影片评分分布', this.buildRatingBuckets(movies, 'rating'))
        this.actorChartOption = this.buildPieOption(
          '演员喜爱度分布',
          this.buildRatingBuckets(actors, 'favorite')
        )
        const tagData = this.buildTagDistribution(tags)
        const tagOption = this.buildPieOption('标签使用分布', tagData, {
          cursor: 'pointer',
        })
        this.tagChartOption = tagOption
      } catch (err) {
        console.error('Failed to load dashboard data:', err)
        this.error = '数据加载失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    buildRatingBuckets(list, field) {
      const buckets = RATING_BUCKETS.map((bucket) => ({ ...bucket, value: 0 }))
      list.forEach((item) => {
        const rawValue = Number(item?.[field])
        if (Number.isFinite(rawValue)) {
          const bucket = buckets.find((range) => rawValue >= range.min && rawValue < range.max)
          if (bucket) {
            bucket.value += 1
          }
        }
      })
      return buckets
        .filter((bucket) => bucket.value > 0)
        .map((bucket) => ({
          name: bucket.label,
          value: bucket.value,
        }))
    },
    buildTagDistribution(tags) {
      if (!Array.isArray(tags) || tags.length === 0) {
        return []
      }
      const sorted = [...tags].sort((a, b) => (b.count || 0) - (a.count || 0))
      const main = sorted.slice(0, 8).map((item) => ({
        name: item.tag,
        value: item.count || 0,
      }))
      const othersTotal = sorted.slice(8).reduce((sum, item) => sum + (item.count || 0), 0)
      if (othersTotal > 0) {
        main.push({
          name: '其他标签',
          value: othersTotal,
        })
      }
      return main.filter((segment) => segment.value > 0)
    },
    buildPieOption(title, data, seriesOverrides = {}) {
      if (!data.length) {
        return null
      }
      return {
        title: {
          text: title,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 600,
          },
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)',
        },
        legend: {
          orient: 'vertical',
          left: 'left',
        },
        series: [
          {
            name: title,
            type: 'pie',
            radius: ['40%', '65%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2,
            },
            label: {
              show: false,
              position: 'center',
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 18,
                fontWeight: 'bold',
              },
            },
            labelLine: {
              show: false,
            },
            data,
            ...seriesOverrides,
          },
        ],
      }
    },
    handleTagChartClick(params) {
      const tagName = params?.data?.name
      if (!tagName || tagName === '其他标签') {
        return
      }
      this.$router.push(`/tags/${encodeURIComponent(tagName)}`)
    },
    formatRating(value) {
      if (typeof value !== 'number') {
        return '暂无评分'
      }
      return value.toFixed(1)
    },
    formatDate(dateString) {
      if (!dateString) {
        return '日期未知'
      }
      const date = new Date(dateString)
      if (Number.isNaN(date.getTime())) {
        return dateString
      }
      return date.toLocaleDateString()
    },
  },
  created() {
    this.fetchDashboardData()
  },
}
</script>

<style scoped>
.dashboard-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 30px 20px 60px;
  color: var(--primary-color);
}

.dashboard-intro h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 600;
  text-shadow: var(--shadow-sm);
}

.dashboard-intro p {
  margin: 8px 0 24px;
  color: var(--secondary-color);
  font-size: 15px;
}

.dashboard-state {
  margin-top: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
  margin-bottom: 36px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 36px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  background: var(--bg-gradient-light);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: var(--bg-gradient-medium);
  color: var(--primary-color);
  font-size: 30px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  font-size: 14px;
  color: var(--secondary-color);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-color);
}

.panels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.panel {
  padding: 24px;
  border-radius: 16px;
  background: var(--bg-gradient-light);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}

.chart-panel {
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  flex: 1;
  margin-top: 20px;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pie-chart {
  width: 100%;
  height: 320px;
}

.panel-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.panel-header small {
  display: block;
  margin-top: 4px;
  color: var(--secondary-color);
  font-size: 12px;
}

.panel-list {
  list-style: none;
  margin: 20px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.panel-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.panel-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.item-title {
  font-weight: 600;
  font-size: 15px;
  color: var(--primary-color);
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--secondary-color);
  font-size: 13px;
}

.item-meta .material-icons {
  font-size: 18px;
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 20px 16px 40px;
  }

  .stat-card {
    padding: 16px;
  }

  .chart-wrapper {
    min-height: 280px;
  }

  .panel {
    padding: 20px;
  }
}
</style>
