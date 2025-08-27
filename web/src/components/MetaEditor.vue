<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`编辑${getTypeName()}信息`"
    width="80%"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" label-width="100px" :rules="rules" ref="formRef">
      <!-- 通用字段 -->
      <el-form-item label="标题" prop="title" v-if="type !== 'actor'">
        <el-input v-model="formData.title" :placeholder="`请输入${getTypeName()}标题`"></el-input>
      </el-form-item>

      <el-form-item label="姓名" prop="name" v-if="type === 'actor'">
        <el-input v-model="formData.name" placeholder="请输入演员姓名"></el-input>
      </el-form-item>

      <!-- Movie 特有字段 -->
      <template v-if="type === 'movie'">
        <el-form-item label="演员" prop="actors">
          <el-input v-model="formData.actors" placeholder="请输入演员，用逗号分隔"></el-input>
        </el-form-item>

        <el-form-item label="评分" prop="rating">
          <el-input-number
            v-model="formData.rating"
            :min="0"
            :max="5"
            :precision="1"
            placeholder="请输入评分(0-5)"
          ></el-input-number>
        </el-form-item>

        <el-form-item label="排行" prop="order">
          <el-input-number
            v-model="formData.order"
            :min="1"
            :max="999"
            placeholder="请输入排行"
          ></el-input-number>
        </el-form-item>
      </template>

      <!-- Actor 特有字段 -->
      <template v-if="type === 'actor'">
        <el-form-item label="出生日期" prop="birth">
          <el-input v-model="formData.birth" placeholder="请输入出生日期"></el-input>
        </el-form-item>

        <el-form-item label="出道日期" prop="debut">
          <el-input v-model="formData.debut" placeholder="请输入出道日期"></el-input>
        </el-form-item>

        <el-form-item label="喜爱度" prop="favorite">
          <el-input-number
            v-model="formData.favorite"
            :min="1"
            :max="5"
            :precision="0"
            placeholder="请输入喜爱度(1-5)"
          ></el-input-number>
        </el-form-item>
      </template>

      <!-- Post 特有字段 -->
      <template v-if="type === 'post'">
        <el-form-item label="作者" prop="author">
          <el-input v-model="formData.author" placeholder="请输入作者"></el-input>
        </el-form-item>

        <el-form-item label="发布日期" prop="date">
          <el-date-picker
            v-model="formData.date"
            type="date"
            placeholder="选择发布日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="摘要" prop="excerpt">
          <el-input
            v-model="formData.excerpt"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要"
          ></el-input>
        </el-form-item>
      </template>

      <!-- 通用字段 -->
      <el-form-item label="标签" prop="tags" v-if="type !== 'actor'">
        <el-input v-model="formData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
      </el-form-item>

      <el-form-item label="描述" prop="description" v-if="type === 'movie'">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入描述"
        ></el-input>
      </el-form-item>

      <!-- 封面图片上传 -->
      <el-form-item label="封面图片" prop="cover">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleImageChange"
          :file-list="imageFileList"
          accept="image/*"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <template #tip>
            <div class="el-upload__tip">只能上传图片文件，且不超过2MB</div>
          </template>
        </el-upload>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import axios from 'axios'
import { UploadFilled } from '@element-plus/icons-vue'

export default {
  name: 'MetaEditor',
  components: {
    UploadFilled,
  },
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      required: true,
      validator: (value) => ['movie', 'actor', 'post'].includes(value),
    },
    data: {
      type: Object,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      formData: {},
      imageFileList: [],
      selectedImageFile: null,
      saving: false,
      rules: {
        title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        actors: [{ required: true, message: '请输入演员信息', trigger: 'blur' }],
        author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
        date: [{ required: true, message: '请选择发布日期', trigger: 'change' }],
      },
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible
      },
      set(value) {
        this.$emit('update:visible', value)
      },
    },
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        this.initFormData()
      }
    },
  },
  methods: {
    getTypeName() {
      const typeNames = {
        movie: '影片',
        actor: '演员',
        post: '文章',
      }
      return typeNames[this.type] || '内容'
    },

    initFormData() {
      // 根据类型初始化表单数据
      this.formData = { ...this.data }

      // 为actor设置喜爱度默认值
      if (this.type === 'actor' && !this.formData.favorite) {
        this.formData.favorite = 1
      }

      // 处理标签字段
      if (this.formData.tags && Array.isArray(this.formData.tags)) {
        this.formData.tags = this.formData.tags.join(', ')
      }

      // 清空图片相关数据
      this.imageFileList = []
      this.selectedImageFile = null
    },

    handleImageChange(file) {
      this.selectedImageFile = file.raw
      this.imageFileList = [file]
    },

    async handleSave() {
      try {
        await this.$refs.formRef.validate()
        this.saving = true

        const formData = new FormData()

        // 根据类型添加不同的字段
        if (this.type === 'movie') {
          formData.append('title', this.formData.title)
          formData.append('actors', this.formData.actors)
          formData.append('description', this.formData.description)
          formData.append('rating', this.formData.rating)
          formData.append('order', this.formData.order)
          formData.append('tags', this.formData.tags)
        } else if (this.type === 'actor') {
          formData.append('name', this.formData.name)
          formData.append('birth', this.formData.birth)
          formData.append('debut', this.formData.debut)
          formData.append('favorite', this.formData.favorite)
        } else if (this.type === 'post') {
          formData.append('title', this.formData.title)
          formData.append('author', this.formData.author)
          formData.append('date', this.formData.date)
          formData.append('excerpt', this.formData.excerpt)
          formData.append('tags', this.formData.tags)
        }

        // 如果有图片，添加到表单数据中
        if (this.selectedImageFile) {
          formData.append('image', this.selectedImageFile)
        }

        // 调用对应的API接口
        const apiUrl = this.getApiUrl()
        const response = await axios.put(apiUrl, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        if (response.data.success) {
          this.$message.success(`${this.getTypeName()}信息已成功更新！`)
          this.$emit('saved', response.data)
          this.dialogVisible = false
        } else {
          this.$message.error('更新失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error updating meta:', error)
        this.$message.error('更新失败，请稍后再试！')
      } finally {
        this.saving = false
      }
    },

    getApiUrl() {
      const apiUrls = {
        movie: `/api/update-movie/${this.id}`,
        actor: `/api/update-actor/${this.id}`,
        post: `/api/update-post/${this.id}`,
      }
      return apiUrls[this.type]
    },

    handleCancel() {
      this.dialogVisible = false
      this.$emit('cancelled')
    },
  },
}
</script>

<style scoped>
.upload-demo {
  width: 100%;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 7px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
