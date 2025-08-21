<template>
  <div class="movie-detail">
    <!-- 标题和编辑按钮 -->
    <div class="title-container">
      <h1>{{ movie.title }}</h1>
      <button @click="openEditDialog" class="edit-movie-button">
        <el-icon><Edit /></el-icon>
      </button>
    </div>
    <img :src="movie.cover" alt="封面" class="cover" @error="setDefaultCover($event)" />
    <p>
      <strong>主演：</strong>
      <span v-if="movie.actors">
        <el-tag
          v-for="(actor, index) in movie.actors.split(', ')"
          :key="index"
          :type="getActorTagType(actor.trim())"
          class="actor-tag"
          @click="goToActor(actor.trim())"
        >
          {{ actor }}
        </el-tag>
      </span>
      <span v-else>暂无演员信息</span>
    </p>
    <!-- 评分 -->
    <div class="rating">
      <strong>评分：</strong>
      <span v-for="i in 5" :key="i" class="star">
        <span class="material-icons" :class="{ filled: i <= movie.rating }">
          {{ i <= movie.rating ? 'star' : 'star_border' }}
        </span>
      </span>
    </div>
    <p>
      <strong>标签：</strong>
      <span v-if="movie.tags">
        <el-tag
          v-for="(tag, index) in movie.tags"
          :key="index"
          :type="getTagType(tag.trim())"
          effect="plain"
          class="tag-item"
          @click="goToTagDetail(tag.trim())"
        >
          {{ tag }}
        </el-tag>
      </span>
      <span v-else>暂无标签信息</span>
    </p>
    <p><strong>简介：</strong>{{ movie.description }}</p>

    <!-- 显示 Markdown 正文 -->
    <div v-html="movie.body_html" class="content"></div>

    <!-- 上一页、下一页按钮 -->
    <div class="navigation">
      <button @click="navigate(-1)" :disabled="!prevMovie">上一页</button>
      <button @click="goBack">返回</button>
      <button @click="navigate(1)" :disabled="!nextMovie">下一页</button>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑影片信息" width="80%">
      <el-form :model="editFormData" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="editFormData.title" placeholder="请输入影片标题"></el-input>
        </el-form-item>
        <el-form-item label="演员">
          <el-input v-model="editFormData.actors" placeholder="请输入演员，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="editFormData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="editFormData.description"
            type="textarea"
            placeholder="请输入影片简介"
          ></el-input>
        </el-form-item>
        <el-form-item label="评分">
          <el-input v-model="editFormData.rating" placeholder="请输入评分(0-5)"></el-input>
        </el-form-item>
        <el-form-item label="封面图片（可选）">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleEditImageChange"
            :file-list="editImageFileList"
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
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateMovie">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { Edit, UploadFilled } from '@element-plus/icons-vue'
export default {
  name: 'MovieDetail',
  data() {
    return {
      movie: {},
      prevMovie: null,
      nextMovie: null,
      editDialogVisible: false, // 控制编辑对话框的显示状态
      editFormData: {}, // 当前正在编辑的影片数据
      editImageFileList: [], // 编辑时的图片文件列表
      selectedEditImageFile: null, // 编辑时选中的图片文件
    }
  },
  components: {
    Edit,
    UploadFilled,
  },
  async created() {
    const { id } = this.$route.params
    const allMovies = await this.fetchMovies()
    const currentIndex = allMovies.findIndex((m) => m.id === id)

    if (currentIndex !== -1) {
      this.movie = allMovies[currentIndex]
      this.prevMovie = currentIndex > 0 ? allMovies[currentIndex - 1] : null
      this.nextMovie = currentIndex < allMovies.length - 1 ? allMovies[currentIndex + 1] : null
    }
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get('/api/movies') // 调用后端 API [[2]]
        return response.data // 返回电影列表
      } catch (error) {
        console.error('请求失败:', error)
      }
    },
    openEditDialog() {
      this.editFormData = { ...this.movie } // 复制当前影片的数据
      this.editDialogVisible = true // 打开编辑对话框
      this.editImageFileList = [] // 清空图片列表
      this.selectedEditImageFile = null // 清空选中的图片
    },
    handleEditImageChange(file) {
      this.selectedEditImageFile = file.raw
      this.editImageFileList = [file]
    },
    async updateMovie() {
      try {
        const formData = new FormData()
        formData.append('title', this.editFormData.title)
        formData.append('actors', this.editFormData.actors)
        formData.append('tags', this.editFormData.tags)
        formData.append('description', this.editFormData.description)
        formData.append('rating', this.editFormData.rating)

        // 如果有图片，添加到表单数据中
        if (this.selectedEditImageFile) {
          formData.append('image', this.selectedEditImageFile)
        }

        const response = await axios.put(`/api/update-movie/${this.editFormData.id}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        if (response.data.success) {
          this.$message.success('影片信息已成功更新！')
          this.editDialogVisible = false // 关闭对话框

          // 刷新整个页面
          location.reload() // 强制刷新页面
        } else {
          this.$message.error('更新失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error updating movie:', error)
        this.$message.error('更新失败，请稍后再试！')
      }
    },
    setDefaultCover(event) {
      event.target.src = '/imgs/default_cover.jpg' // 默认图片路径
    },
    navigate(direction) {
      const targetMovie = direction === -1 ? this.prevMovie : this.nextMovie
      if (targetMovie) {
        this.$router.push({
          name: 'MovieDetail',
          params: { id: targetMovie.id },
        })
      }
    },
    goBack() {
      this.$router.go(-1) // 返回上一页 [[7]]
    },
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
    },
    goToActor(name) {
      console.log('跳转到演员详情页，演员姓名:', name) // 调试信息
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
    },
    goToTagDetail(tagName) {
      this.$router.push(`/tags/${tagName}`) // 跳转到标签详情页面
    },
    getActorTagType(actorName) {
      // 根据演员名字生成固定的类型映射 [[6]]
      const types = ['success', 'info', 'warning', 'danger']
      const typeIndex = Math.abs(this.hashCode(actorName)) % types.length
      return types[typeIndex]
    },
    getTagType(tag) {
      // 根据标签名字生成固定的类型映射 [[6]]
      const types = ['success', 'info', 'warning', 'danger']
      const typeIndex = Math.abs(this.hashCode(tag)) % types.length
      return types[typeIndex]
    },
    hashCode(str) {
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }
      return hash
    },
  },
}
</script>

<style scoped>
.logo img {
  width: 100px;
  cursor: pointer;
}

.title-container {
  display: flex;
  flex-direction: row;
}

.movie-detail {
  padding: 0 10px;
  max-width: 600px;
  margin: auto;
}

.actor-tag {
  margin-right: 5px;
  cursor: pointer;
}

.tag-item {
  margin-right: 5px;
}

.tag-item:hover {
  cursor: pointer;
  background-color: #f0f0f0; /* 鼠标悬停时的背景色 */
}

.cover {
  max-width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  margin-top: 20px;
}
.navigation {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}
button {
  padding: 10px 20px;
  cursor: pointer;
  position: relative;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
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

.edit-movie-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #409eff;
}
</style>
