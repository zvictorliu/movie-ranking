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
  },
}
</script>

<style scoped>
.actor-detail {
  text-align: left;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.title-container h1 {
  margin: 0;
  flex: 1;
}

.edit-buttons {
  display: flex;
  gap: 12px;
}

.cover {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
}

.content ::v-deep(img) {
  /* 深度选择器，确保样式应用于子组件的 img 元素 */
  max-width: 100%; /* 确保图片宽度不超过父容器 */
  height: auto; /* 保持图片比例 */
  border-radius: 10px; /* 添加圆角效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 [[8]] */
}

.rating {
  display: flex;
  align-items: center;
  gap: 2px; /* 星星之间的间距 */
}

.star {
  font-size: 20px; /* 星星图标的大小 */
  color: #ccc; /* 默认颜色为灰色 */
}

.star .material-icons.filled {
  color: #ffca28; /* 填充的星星颜色为黄色 */
}

button {
  padding: 10px 20px;
  cursor: pointer;
  position: relative;
}

.edit-meta-button,
.edit-body-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 2px solid;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: white;
}

.edit-meta-button {
  color: #409eff;
  border-color: #409eff;
}

.edit-meta-button:hover {
  background: #409eff;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.edit-body-button {
  color: #67c23a;
  border-color: #67c23a;
}

.edit-body-button:hover {
  background: #67c23a;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
}

.button-text {
  font-size: 12px;
  font-weight: 600;
}

/* 编辑正文对话框样式 */
:deep(.body-editor-dialog .el-dialog) {
  height: 90vh;
}

:deep(.body-editor-dialog .el-dialog__body) {
  height: calc(90vh - 120px);
  padding: 0;
}
</style>
