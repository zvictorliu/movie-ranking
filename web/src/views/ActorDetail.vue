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
    <img :src="actor.cover" alt="演员封面" class="cover" @error="setDefaultCover($event)" />
    <p><strong>出生日期：</strong>{{ actor.birth }}</p>
    <p><strong>出道日期：</strong>{{ actor.debut }}</p>
    <div class="favorite-section">
      <strong>喜爱度：</strong>
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
    </div>

    <!-- 渲染正文内容 -->
    <div class="content" v-if="!editBodyDialogVisible">
      <MarkdownRender :content="actor.body" />
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
    <button @click="goBack">返回</button>

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
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.actor-detail h1 {
  color: #667eea;
  font-size: 2rem;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.actor-detail p {
  color: #555;
  line-height: 1.6;
  margin-bottom: 15px;
}

.actor-detail strong {
  color: #667eea;
  font-weight: 600;
}

/* title-container 样式已移至 article-title.scss */

.cover {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
  border-radius: 12px;
  border: 2px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transition: all 0.3s ease;
}

.cover:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
  transform: translateY(-2px);
}

.content {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.15);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.08);
}

button {
  padding: 12px 24px;
  cursor: pointer;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  margin-top: 20px;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

/* 编辑按钮样式已移至 article-title.scss */

/* 喜爱度样式 */
.favorite-section {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 20px 0;
  padding: 15px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.favorite-section strong {
  color: #667eea;
}

.favorite-hearts {
  display: flex;
  gap: 5px;
}

.heart {
  cursor: pointer;
  transition: all 0.2s ease;
}

.heart .material-icons {
  font-size: 28px;
}

.heart.filled .material-icons {
  color: #e91e63;
  text-shadow: 0 2px 4px rgba(233, 30, 99, 0.3);
}

.heart.empty .material-icons {
  color: #ddd;
}

.heart:hover {
  transform: scale(1.2);
}

.heart:hover .material-icons {
  color: #e91e63;
}

/* 编辑正文对话框样式 */
:deep(.body-editor-dialog .el-dialog) {
  height: 90vh;
}

:deep(.body-editor-dialog .el-dialog__body) {
  height: calc(90vh - 120px);
  padding: 0;
}

/* 暗色模式 */
body.dark-mode .actor-detail {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

body.dark-mode .actor-detail h1 {
  background: linear-gradient(135deg, #a8b5f0 0%, #c8a5d8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

body.dark-mode .actor-detail p {
  color: #b0b0b0;
}

body.dark-mode .actor-detail strong {
  color: #a8b5f0;
}

body.dark-mode .cover {
  border-color: rgba(168, 181, 240, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

body.dark-mode .content {
  background: #2d2d2d;
  border-color: rgba(168, 181, 240, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

body.dark-mode button {
  background: linear-gradient(135deg, #a8b5f0 0%, #c8a5d8 100%);
}

body.dark-mode .favorite-section {
  background: linear-gradient(135deg, rgba(168, 181, 240, 0.1) 0%, rgba(200, 165, 216, 0.1) 100%);
  border-color: rgba(168, 181, 240, 0.2);
}

body.dark-mode .favorite-section strong {
  color: #a8b5f0;
}
</style>
