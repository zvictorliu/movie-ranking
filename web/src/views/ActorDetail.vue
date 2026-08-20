<template>
  <div class="actor-detail">
    <div class="title-container">
      <h1>{{ actor.name }}</h1>
      <div class="edit-buttons">
        <el-tooltip content="编辑演员信息" placement="top">
          <button @click="openEditMetaDialog" class="edit-meta-button">
            <el-icon><Setting /></el-icon>
            <span class="button-text">信息</span>
          </button>
        </el-tooltip>
        <el-tooltip content="编辑正文内容" placement="top">
          <button @click="openEditBodyDialog" class="edit-body-button">
            <el-icon><Document /></el-icon>
            <span class="button-text">正文</span>
          </button>
        </el-tooltip>
      </div>
    </div>

    <div class="article-body">
      <aside v-if="actor.cover || hasMetaSection" class="infobox">
        <div class="infobox-header">{{ actor.name }}</div>
        <div class="infobox-photo">
          <img
            :src="actor.cover"
            :alt="actor.name ? `${actor.name} 的照片` : '演员封面'"
            class="cover"
            @error="setDefaultCover($event)"
          />
        </div>
        <table v-if="hasMetaSection" class="infobox-table">
          <tbody>
            <tr v-for="item in metaInfoItems" :key="item.label">
              <th scope="row">{{ item.label }}</th>
              <td>{{ item.value }}</td>
            </tr>
            <tr v-if="shouldShowFavorite">
              <th scope="row">喜爱度</th>
              <td>
                <span class="favorite-hearts">
                  <span
                    v-for="i in 5"
                    :key="i"
                    class="heart"
                    :class="{ filled: i <= actor.favorite, empty: i > actor.favorite }"
                    @click="updateFavorite(i)"
                  >
                    <span class="material-icons">
                      {{ i <= actor.favorite ? 'favorite' : 'favorite_border' }}
                    </span>
                  </span>
                </span>
              </td>
            </tr>
            <tr v-if="socialLinks.length">
              <th scope="row">社媒链接</th>
              <td>
                <span class="social-links-list">
                  <a
                    v-for="link in socialLinks"
                    :key="link.type"
                    class="social-link"
                    :href="link.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    :title="link.title"
                    :aria-label="link.ariaLabel"
                  >
                    <i
                      :class="['social-icon', `social-icon--${link.type}`, 'fa-brands', link.iconClass]"
                      aria-hidden="true"
                    ></i>
                  </a>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </aside>

      <!-- 渲染正文内容 -->
      <div class="content" v-if="!editBodyDialogVisible">
        <MarkdownRender :content="actor.body" />
      </div>
    </div>

    <!-- 编辑正文对话框 -->
    <el-dialog
      v-model="editBodyDialogVisible"
      title="编辑正文内容"
      width="90%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      class="body-editor-dialog"
    >
      <LiveEditor
        v-model="actor.body"
        :title="`编辑《${actor.name}》正文`"
        :actor-id="actor.name"
        @saved="onBodySaved"
        @cancelled="editBodyDialogVisible = false"
      />
    </el-dialog>

    <!-- 返回按钮 -->
    <button class="back-button" @click="goBack">返回</button>

    <!-- 编辑元信息对话框 -->
    <MetaEditor
      v-model:visible="editMetaDialogVisible"
      type="actor"
      :data="actor"
      :id="actor.name"
      @saved="onMetaSaved"
      @cancelled="editMetaDialogVisible = false"
    />
  </div>
</template>

<script>
import axios from 'axios'
import { Document, Setting } from '@element-plus/icons-vue'
import LiveEditor from '@/components/LiveEditor.vue'
import MetaEditor from '@/components/MetaEditor.vue'
import MarkdownRender from '@/components/MarkdownRender.vue'

export default {
  name: 'ActorDetailPage',
  components: {
    Document,
    Setting,
    LiveEditor,
    MetaEditor,
    MarkdownRender,
  },
  data() {
    return {
      actor: {},
      editBodyDialogVisible: false, // 控制编辑正文对话框的显示状态
      editMetaDialogVisible: false, // 控制编辑元信息对话框的显示状态
    }
  },
  computed: {
    socialLinks() {
      const links = []
      const mappings = [
        {
          type: 'x',
          value: this.actor?.x,
          iconClass: 'fa-x-twitter',
          title: '前往 X',
          ariaLabel: '打开 X 链接',
        },
        {
          type: 'instagram',
          value: this.actor?.instagram,
          iconClass: 'fa-instagram',
          title: '前往 Instagram',
          ariaLabel: '打开 Instagram 链接',
        },
        {
          type: 'wiki',
          value: this.actor?.wiki,
          iconClass: 'fa-wikipedia-w',
          title: '查看 Wiki',
          ariaLabel: '打开 Wiki 链接',
        },
      ]

      mappings.forEach((item) => {
        const url = this.normalizeLink(item.value)
        if (url) {
          links.push({
            ...item,
            url,
          })
        }
      })

      return links
    },
    metaInfoItems() {
      const items = []
      if (this.actor?.birth) {
        const formattedBirth = this.formatActorDate(this.actor.birth)
        if (formattedBirth) {
          items.push({
            label: '出生日期',
            value: formattedBirth,
          })
        }
      }
      if (this.actor?.debut) {
        const formattedDebut = this.formatActorDate(this.actor.debut)
        if (formattedDebut) {
          items.push({
            label: '出道日期',
            value: formattedDebut,
          })
        }
      }
      return items
    },
    shouldShowFavorite() {
      const favorite = Number(this.actor?.favorite)
      return (
        this.actor?.favorite !== undefined &&
        this.actor?.favorite !== null &&
        !Number.isNaN(favorite)
      )
    },
    hasMetaSection() {
      return (
        this.metaInfoItems.length > 0 ||
        this.shouldShowFavorite ||
        this.socialLinks.length > 0
      )
    },
  },
  async created() {
    const { name } = this.$route.params
    try {
      const response = await axios.get(`/api/actor/${name}`)
      this.actor = response.data
    } catch (error) {
      console.error('请求失败:', error)
    }

    // 监听演员创建事件，因为可能会影响当前演员信息
    this.$eventBus.on('actor-created', () => {
      this.refreshActorData()
    })
  },
  beforeUnmount() {
    // 清理事件监听器
    this.$eventBus.off('actor-created')
  },
  methods: {
    normalizeLink(link) {
      if (!link || typeof link !== 'string') {
        return ''
      }
      const trimmed = link.trim()
      if (!trimmed) {
        return ''
      }
      if (/^https?:\/\//i.test(trimmed)) {
        return trimmed
      }
      return `https://${trimmed}`
    },
    formatActorDate(value) {
      if (value === undefined || value === null) {
        return ''
      }
      const stringValue = String(value).trim()
      if (!stringValue) {
        return ''
      }
      const directMatch = stringValue.match(/(\d{4})\D(\d{1,2})\D(\d{1,2})/)
      if (directMatch) {
        const [, year, month, day] = directMatch
        const paddedMonth = month.padStart(2, '0')
        const paddedDay = day.padStart(2, '0')
        return `${year}-${paddedMonth}-${paddedDay}`
      }
      const parsed = Date.parse(stringValue)
      if (!Number.isNaN(parsed)) {
        return new Date(parsed).toISOString().slice(0, 10)
      }
      return stringValue
    },
    setDefaultCover(event) {
      event.target.src = '/imgs/default_cover.jpg'
    },
    goBack() {
      this.$router.go(-1) // 返回上一页 [[7]]
    },
    openEditBodyDialog() {
      this.editBodyDialogVisible = true // 打开编辑正文对话框
    },
    async onBodySaved(newBody) {
      // 更新本地数据
      this.actor.body = newBody
      this.editBodyDialogVisible = false
    },

    openEditMetaDialog() {
      this.editMetaDialogVisible = true
    },
    onMetaSaved() {
      // 刷新整个页面以显示更新后的信息
      location.reload()
    },
    async updateFavorite(value) {
      try {
        const response = await axios.put(`/api/update-actor-favorite/${this.actor.name}`, {
          favorite: value,
        })
        if (response.data.success) {
          this.actor.favorite = value
          this.$message.success('喜爱度更新成功！')
        } else {
          this.$message.error('更新失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error updating favorite:', error)
        this.$message.error('更新失败，请稍后再试！')
      }
    },
    async refreshActorData() {
      const { name } = this.$route.params
      try {
        const response = await axios.get(`/api/actor/${name}`)
        this.actor = response.data
      } catch (error) {
        console.error('请求失败:', error)
      }
    },
  },
}
</script>

<style scoped>
.actor-detail {
  text-align: left;
  max-width: 960px;
  margin: 0 auto;
  padding: 30px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
}

.actor-detail :deep(.title-container) {
  border-bottom: 1px solid var(--border-medium);
  padding-bottom: 12px;
  margin-bottom: 16px;
  align-items: flex-end;
}

.actor-detail h1 {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 0;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.actor-detail p {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 15px;
}

.actor-detail strong {
  color: var(--primary-color);
  font-weight: 600;
}

.article-body::after {
  content: '';
  display: block;
  clear: both;
}

.infobox {
  float: right;
  width: 260px;
  margin: 0 0 1.25rem 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-medium);
  font-size: 0.875rem;
  line-height: 1.45;
}

.infobox-header {
  font-weight: 700;
  font-size: 1.05rem;
  text-align: center;
  padding: 10px 8px;
  background: var(--bg-gradient-medium);
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
}

.infobox-photo {
  padding: 8px 8px 4px;
  text-align: center;
}

.cover {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0 auto;
  border: 1px solid var(--border-light);
}

.infobox-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 4px;
}

.infobox-table th,
.infobox-table td {
  padding: 7px 10px;
  border-top: 1px solid var(--border-light);
  vertical-align: top;
}

.infobox-table th {
  width: 36%;
  font-weight: 600;
  text-align: left;
  color: var(--text-secondary);
  background: var(--bg-gradient-light);
  white-space: nowrap;
}

.infobox-table td {
  color: var(--text-secondary);
}

.content {
  color: var(--text-secondary);
  line-height: 1.7;
}

.content :deep(.markdown-render) {
  min-width: 0;
}

.content :deep(.markdown-content) > *:first-child {
  margin-top: 0;
}

.content :deep(.movie-preview),
.content :deep(.markdown-inline-image) {
  clear: right;
}

.back-button {
  padding: 12px 24px;
  cursor: pointer;
  position: relative;
  background: var(--btn-primary-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  margin-top: 20px;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.favorite-hearts {
  display: flex;
  gap: 2px;
  flex-wrap: wrap;
}

.heart {
  cursor: pointer;
  transition: all 0.2s ease;
}

.heart .material-icons {
  font-size: 20px;
}

.heart.filled .material-icons {
  color: #e91e63;
}

.heart.empty .material-icons {
  color: #ddd;
}

.heart:hover {
  transform: scale(1.15);
}

.heart:hover .material-icons {
  color: #e91e63;
}

.social-links-list {
  display: inline-flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.social-link {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  transition: color 0.2s ease;
}

.social-link:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 3px;
  border-radius: 6px;
}

.social-icon {
  font-size: 18px;
  line-height: 1;
  transition: transform 0.2s ease;
}

.social-link:hover .social-icon,
.social-link:focus-visible .social-icon {
  transform: translateY(-1px);
}

.social-icon--x {
  color: #000;
}

.social-link:hover .social-icon--x,
.social-link:focus-visible .social-icon--x {
  color: #222;
}

.social-icon--instagram {
  background: linear-gradient(135deg, #feda75, #fa7e1e, #d62976, #962fbf);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.social-link:hover .social-icon--instagram,
.social-link:focus-visible .social-icon--instagram {
  filter: brightness(1.1);
}

.social-icon--wiki {
  color: #3366cc;
}

.social-link:hover .social-icon--wiki,
.social-link:focus-visible .social-icon--wiki {
  color: #1f4d99;
}

:deep(.body-editor-dialog .el-dialog) {
  height: 90vh;
}

:deep(.body-editor-dialog .el-dialog__body) {
  height: calc(90vh - 120px);
  padding: 0;
}

@media (max-width: 768px) {
  .infobox {
    float: none;
    width: 100%;
    max-width: 280px;
    margin: 0 auto 1.5rem;
  }

  .actor-detail {
    padding: 20px 16px;
  }
}

body.dark-mode .social-icon--x {
  color: #fff;
}

body.dark-mode .social-link:hover .social-icon--x,
body.dark-mode .social-link:focus-visible .social-icon--x {
  color: #ddd;
}
</style>
