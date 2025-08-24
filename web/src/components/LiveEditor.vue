<template>
  <div class="live-editor">
    <div class="editor-header">
      <h3>{{ title }}</h3>
      <div class="editor-actions">
        <el-button @click="saveContent" type="primary" :loading="saving"> 保存 </el-button>
        <el-button @click="cancelEdit">取消</el-button>
      </div>
    </div>

    <div class="editor-container">
      <MdEditor
        v-model="content"
        :toolbars="toolbars"
        :preview="preview"
        :codeTheme="codeTheme"
        :theme="theme"
        @onSave="saveContent"
        @onUploadImg="onUploadImg"
        class="md-editor"
      />
    </div>
  </div>
</template>

<script>
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import axios from 'axios'

export default {
  name: 'LiveEditor',
  components: {
    MdEditor,
  },
  props: {
    modelValue: {
      type: String,
      default: '',
    },
    title: {
      type: String,
      default: '编辑内容',
    },
    movieId: {
      type: String,
      default: '',
    },
    actorId: {
      type: String,
      default: '',
    },
    postSlug: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      content: this.modelValue,
      saving: false,
      preview: true,
      codeTheme: 'github',
      theme: 'light',
      toolbars: [
        'bold',
        'underline',
        'italic',
        'strikethrough',
        'title',
        'sub',
        'sup',
        'quote',
        'unordered-list',
        'ordered-list',
        'task-list',
        '-',
        'code',
        'code-block',
        'link',
        'image',
        'table',
        'mermaid',
        'katex',
        '-',
        'preview',
        'previewOnly',
        'fullscreen',
        'save',
      ],
    }
  },
  watch: {
    modelValue(newVal) {
      this.content = newVal
    },
  },
  methods: {
    async saveContent() {
      this.saving = true
      try {
        let response

        if (this.movieId) {
          // 保存电影正文
          response = await axios.put(`/api/update-movie-body/${this.movieId}`, {
            body: this.content,
          })
        } else if (this.actorId) {
          // 保存演员正文
          response = await axios.put(`/api/update-actor-body/${this.actorId}`, {
            body: this.content,
          })
        } else if (this.postSlug) {
          // 保存文章正文
          response = await axios.put(`/api/update-post-body/${this.postSlug}`, {
            body: this.content,
          })
        } else {
          throw new Error('未指定编辑类型')
        }

        if (response.data.success) {
          this.$message.success('内容保存成功！')
          this.$emit('update:modelValue', this.content)
          this.$emit('saved', this.content)
        } else {
          this.$message.error('保存失败：' + response.data.message)
        }
      } catch (error) {
        console.error('保存内容失败:', error)
        this.$message.error('保存失败，请稍后再试！')
      } finally {
        this.saving = false
      }
    },

    cancelEdit() {
      this.content = this.modelValue
      this.$emit('cancelled')
    },

    async onUploadImg(files, callback) {
      try {
        // 确定图片类型
        let imageType = 'movie'
        if (this.actorId) {
          imageType = 'actor'
        } else if (this.postSlug) {
          imageType = 'post'
        }

        const uploadPromises = files.map(async (file) => {
          const formData = new FormData()
          formData.append('image', file)
          formData.append('name', file.name)
          formData.append('type', imageType)

          const response = await axios.post('/api/upload-image', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })

          if (response.data.success) {
            return response.data.path
          } else {
            throw new Error(response.data.message)
          }
        })

        const urls = await Promise.all(uploadPromises)
        callback(urls)
      } catch (error) {
        console.error('图片上传失败:', error)
        this.$message.error('图片上传失败：' + error.message)
        callback([])
      }
    },
  },
}
</script>

<style scoped>
.live-editor {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
  background-color: #f5f7fa;
}

.editor-header h3 {
  margin: 0;
  color: #303133;
}

.editor-actions {
  display: flex;
  gap: 8px;
}

.editor-container {
  flex: 1;
  overflow: hidden;
}

.md-editor {
  height: 100%;
  border: none;
}

:deep(.md-editor) {
  border: none;
}

:deep(.md-editor .md-toolbar) {
  border-bottom: 1px solid #e4e7ed;
}

:deep(.md-editor .md-content) {
  border: none;
}
</style>
