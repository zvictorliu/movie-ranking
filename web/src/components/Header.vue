<template>
  <header :class="['app-header', isMobile ? 'mobile-header' : 'desktop-header']">
    <!-- 桌面端 Header -->
    <div v-if="!isMobile" class="desktop-header-content">
      <div class="header-wrapper">
        <div class="logo" @click="goToHome">
          <img src="/home-button.png" alt="Logo" />
        </div>
        <h1 class="title">影片排行榜</h1>
      </div>
      <div class="header-nav">
        <span @click="goToMovies" class="nav-link" title="影片排行页面">影片排行</span>
        <span @click="goToActors" class="nav-link" title="演员列表页面">演员列表</span>
        <span @click="goToTags" class="nav-link" title="标签页页面">标签列表</span>
        <span @click="goToPosts" class="nav-link" title="博客列表页面">博客列表</span>
        <button class="new-button" @click="openMovieDialog">新增影片</button>
        <button class="new-button" @click="openActorDialog">新增演员</button>
        <button class="new-button" @click="openPostDialog">新建博客</button>
        <button class="new-button" @click="openImageDialog">上传封面</button>
        <button class="theme-toggle" @click="toggleTheme">
          <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>
      </div>
    </div>

    <!-- 移动端 Header -->
    <div v-else class="mobile-header-content">
      <div class="header-wrapper">
        <div class="logo" @click="goToHome">
          <img src="/home-button.png" alt="Logo" />
        </div>
        <h1 class="title">影片排行榜</h1>
        <button class="menu-button" @click="toggleMenu">
          <!-- 动态切换图标 -->
          <span class="material-icons">{{ isMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
      <div v-if="isMenuOpen" class="dropdown-menu">
        <span @click="goToMovies" class="nav-link" title="影片排行页面">影片排行</span>
        <span @click="goToActors" class="nav-link" title="演员列表页面">演员列表</span>
        <span @click="goToTags" class="nav-link" title="标签页页面">标签列表</span>
        <span @click="goToPosts" class="nav-link" title="博客列表页面">博客列表</span>
        <button class="new-button" @click="openMovieDialog">新增影片</button>
        <button class="new-button" @click="openActorDialog">新增演员</button>
        <button class="new-button" @click="openPostDialog">新建博客</button>
        <button class="new-button" @click="openImageDialog">上传封面</button>
        <button class="theme-toggle" @click="toggleTheme">
          <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
        </button>
      </div>
    </div>

    <!-- 上传图片浮动窗口 -->
    <el-dialog v-model="imageDialogVisible" title="上传图片" width="80%">
      <el-form :model="imageFormData" label-width="80px">
        <el-form-item label="图片名称">
          <el-input
            v-model="imageFormData.name"
            placeholder="请输入图片名称（不需要包含文件后缀）"
          ></el-input>
        </el-form-item>
        <el-form-item label="图片类型">
          <el-select v-model="imageFormData.type" placeholder="请选择图片类型" style="width: 100%">
            <el-option label="演员" value="actor"></el-option>
            <el-option label="影片" value="movie"></el-option>
            <el-option label="博客" value="post"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择图片">
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
              <div class="el-upload__tip">只能上传jpg/png文件，且不超过2MB</div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="imageDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveImage">上传</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 浮动窗口 -->
    <el-dialog v-model="movieDialogVisible" title="新增影片" width="80%">
      <el-form :model="movieFormData" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="movieFormData.title" placeholder="请输入影片标题"></el-input>
        </el-form-item>
        <el-form-item label="演员">
          <el-input v-model="movieFormData.actors" placeholder="请输入演员，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="movieFormData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="movieFormData.description"
            type="textarea"
            placeholder="请输入影片简介"
          ></el-input>
        </el-form-item>
        <!-- <el-form-item label="封面">
            <el-input v-model="movieFormData.cover" placeholder="请输入封面图片路径"></el-input>
          </el-form-item> -->
        <el-form-item label="order">
          <el-input v-model="movieFormData.order" placeholder="请输入影片顺序"></el-input>
        </el-form-item>
        <el-form-item label="rating">
          <el-input v-model="movieFormData.rating" placeholder="请输入影片评分"></el-input>
        </el-form-item>
        <el-form-item label="封面图片（可选）">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleMovieImageChange"
            :file-list="movieImageFileList"
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
          <el-button @click="movieDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMovie">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 浮动窗口 -->
    <el-dialog v-model="actorDialogVisible" title="新增演员" width="80%">
      <el-form :model="actorFormData" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="actorFormData.name" placeholder="请输入演员姓名"></el-input>
        </el-form-item>
        <el-form-item label="出生日期">
          <el-input
            v-model="actorFormData.birth"
            placeholder="请输入出生日期"
            style="width: 100%"
          ></el-input>
        </el-form-item>
        <el-form-item label="出道日期">
          <el-input
            v-model="actorFormData.debut"
            placeholder="请输入出道日期"
            style="width: 100%"
          ></el-input>
        </el-form-item>
        <el-form-item label="头像图片（可选）">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleActorImageChange"
            :file-list="actorImageFileList"
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
          <el-button @click="actorDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveActor">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 新建博客浮动窗口 -->
    <el-dialog v-model="postDialogVisible" title="新建博客" width="80%">
      <el-form :model="postFormData" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="postFormData.title" placeholder="请输入博客标题"></el-input>
        </el-form-item>
        <el-form-item label="Slug">
          <el-input
            v-model="postFormData.slug"
            placeholder="请输入URL友好的标识符（可选，留空将使用标题自动生成）"
          ></el-input>
          <div v-if="!postFormData.slug.trim() && postFormData.title.trim()" class="slug-preview">
            <small>预览: {{ generateSlugPreview(postFormData.title) }}</small>
          </div>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="postFormData.author" placeholder="请输入作者姓名"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="postFormData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="摘要">
          <el-input
            v-model="postFormData.excerpt"
            type="textarea"
            :rows="3"
            placeholder="请输入博客摘要"
          ></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="postFormData.content"
            type="textarea"
            :rows="10"
            placeholder="请输入博客内容"
          ></el-input>
        </el-form-item>
        <el-form-item label="发布日期">
          <el-date-picker
            v-model="postFormData.date"
            type="date"
            placeholder="选择发布日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="postDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="savePost">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </header>
</template>

<script>
import { useViewStore } from '../store/view'
import axios from 'axios'
import { UploadFilled } from '@element-plus/icons-vue'
export default {
  name: 'AppHeader',
  components: {
    UploadFilled,
  },
  data() {
    return {
      isMobile: false, // 是否显示菜单按钮
      isMenuOpen: false, // 菜单是否展开
      isDarkMode: false, // 是否启用夜间模式
      movieDialogVisible: false, // 控制浮动窗口的显示状态
      movieFormData: {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 10,
        rating: 0,
      },
      actorDialogVisible: false, // 控制浮动窗口的显示状态
      actorFormData: {
        name: '',
        birth: '',
        debut: '',
      },
      imageDialogVisible: false, // 控制图片上传浮动窗口的显示状态
      imageFormData: {
        name: '',
        type: '',
      },
      imageFileList: [], // 图片文件列表
      selectedImageFile: null, // 选中的图片文件
      movieImageFileList: [], // 新增影片图片文件列表
      selectedMovieImageFile: null, // 新增影片选中的图片文件
      actorImageFileList: [], // 新增演员图片文件列表
      selectedActorImageFile: null, // 新增演员选中的图片文件
      postDialogVisible: false, // 控制博客浮动窗口的显示状态
      postFormData: {
        title: '',
        slug: '',
        author: '',
        tags: '',
        excerpt: '',
        content: '',
        date: '',
      },
    }
  },
  setup() {
    const viewStore = useViewStore()
    return { viewStore }
  },
  methods: {
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
      this.isMenuOpen = false // 关闭菜单
    },
    goToMovies() {
      this.$router.push({ name: 'MoviesPage' }) // 跳转到影片排行页面
      this.isMenuOpen = false // 关闭菜单
    },
    goToActors() {
      this.$router.push({ name: 'ActorsPage' }) // 跳转到演员列表页面
      this.isMenuOpen = false // 关闭菜单
    },
    goToTags() {
      this.$router.push('/tags') // 跳转到标签页面
      this.isMenuOpen = false // 关闭菜单
    },
    goToPosts() {
      this.$router.push({ name: 'PostsPage' }) // 跳转到博客列表页面
      this.isMenuOpen = false // 关闭菜单
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen // 切换菜单状态
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode // 切换夜间模式
      document.body.classList.toggle('dark-mode', this.isDarkMode) // 动态切换 body 的主题类 [[7]]
    },
    checkScreenWidth() {
      this.isMobile = window.innerWidth < 768 // 当屏幕宽度小于 768px 时显示菜单按钮 [[1]]
    },
    toggleView() {
      this.viewStore.toggleView()
    },
    openMovieDialog() {
      this.movieDialogVisible = true // 打开浮动窗口
    },
    handleMovieImageChange(file) {
      this.selectedMovieImageFile = file.raw
      this.movieImageFileList = [file]
    },
    handleActorImageChange(file) {
      this.selectedActorImageFile = file.raw
      this.actorImageFileList = [file]
    },
    resetMovieForm() {
      this.movieFormData = {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 1,
        rating: 0,
      }
      this.movieImageFileList = []
      this.selectedMovieImageFile = null
    },
    openActorDialog() {
      this.actorDialogVisible = true
    },
    resetActorForm() {
      this.actorFormData = {
        name: '',
        birth: '',
        debut: '',
      }
      this.actorImageFileList = []
      this.selectedActorImageFile = null
    },
    openImageDialog() {
      this.imageDialogVisible = true
    },
    openPostDialog() {
      this.postDialogVisible = true
      // 设置默认日期为今天
      if (!this.postFormData.date) {
        this.postFormData.date = new Date().toISOString().split('T')[0]
      }
    },
    resetImageForm() {
      this.imageFormData = {
        name: '',
        type: '',
      }
      this.imageFileList = []
      this.selectedImageFile = null
    },
    resetPostForm() {
      this.postFormData = {
        title: '',
        slug: '',
        author: '',
        tags: '',
        excerpt: '',
        content: '',
        date: new Date().toISOString().split('T')[0], // 默认设置为今天
      }
    },
    generateSlugPreview(title) {
      if (!title) return ''
      return title
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')
    },
    handleImageChange(file) {
      this.selectedImageFile = file.raw
      this.imageFileList = [file]
    },
    async saveMovie() {
      try {
        const formData = new FormData()
        formData.append('title', this.movieFormData.title)
        formData.append('actors', this.movieFormData.actors)
        formData.append('tags', this.movieFormData.tags)
        formData.append('description', this.movieFormData.description)
        formData.append('order', this.movieFormData.order)
        formData.append('rating', this.movieFormData.rating)

        // 如果有图片，添加到表单数据中
        if (this.selectedMovieImageFile) {
          formData.append('image', this.selectedMovieImageFile)
        }

        const response = await axios.post('/api/create-movie', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        if (response.data.success) {
          this.$message.success('影片已成功创建！')
          this.movieDialogVisible = false
          this.resetMovieForm()
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
    async saveActor() {
      try {
        const formData = new FormData()
        formData.append('name', this.actorFormData.name)
        formData.append('birth', this.actorFormData.birth)
        formData.append('debut', this.actorFormData.debut)

        // 如果有图片，添加到表单数据中
        if (this.selectedActorImageFile) {
          formData.append('image', this.selectedActorImageFile)
        }

        const response = await axios.post('/api/create-actor', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        if (response.data.success) {
          this.$message.success('演员已成功创建！')
          this.actorDialogVisible = false
          this.resetActorForm()
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
    async saveImage() {
      if (!this.selectedImageFile) {
        this.$message.error('请选择要上传的图片！')
        return
      }
      if (!this.imageFormData.name.trim()) {
        this.$message.error('请输入图片名称！')
        return
      }
      if (!this.imageFormData.type) {
        this.$message.error('请选择图片类型！')
        return
      }

      try {
        const formData = new FormData()
        formData.append('image', this.selectedImageFile)
        formData.append('name', this.imageFormData.name)
        formData.append('type', this.imageFormData.type)

        const response = await axios.post('/api/upload-image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        if (response.data.success) {
          this.$message.success('图片上传成功！')
          this.imageDialogVisible = false
          this.resetImageForm()
        } else {
          this.$message.error('上传失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('上传失败，请稍后再试！')
      }
    },
    async savePost() {
      try {
        // 验证必填字段
        if (!this.postFormData.title.trim()) {
          this.$message.error('请输入博客标题！')
          return
        }
        if (!this.postFormData.author.trim()) {
          this.$message.error('请输入作者姓名！')
          return
        }
        if (!this.postFormData.content.trim()) {
          this.$message.error('请输入博客内容！')
          return
        }

        // 生成slug（URL友好的标题）
        const generateSlug = (title) => {
          return title
            .toLowerCase()
            .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
            .replace(/-+/g, '-')
            .replace(/^-|-$/g, '')
        }

        // 优先使用用户输入的slug，如果没有输入则使用标题生成
        const slug = this.postFormData.slug.trim() || generateSlug(this.postFormData.title)

        const postData = {
          slug: slug,
          title: this.postFormData.title,
          author: this.postFormData.author,
          tags: this.postFormData.tags
            ? this.postFormData.tags.split(',').map((tag) => tag.trim())
            : [],
          excerpt: this.postFormData.excerpt,
          content: this.postFormData.content,
          date: this.postFormData.date || new Date().toISOString().split('T')[0],
        }

        const response = await axios.post('/api/create-post', postData)

        if (response.data.success) {
          this.$message.success('博客已成功创建！')
          this.postDialogVisible = false
          this.resetPostForm()
          // 可以选择跳转到博客列表页面
          this.$router.push({ name: 'PostsPage' })
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
  },
  created() {
    this.checkScreenWidth() // 初始化检查屏幕宽度
    window.addEventListener('resize', this.checkScreenWidth) // 监听窗口大小变化
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenWidth) // 移除监听器
  },
}
</script>

<style scoped>
.app-header {
  background-color: #f8f8f8;
  padding: 10px 0 0 0;
  align-items: center;
  display: flex;
}

.header-wrapper {
  display: flex;
  align-items: left;
}

.logo img {
  width: 50px;
  cursor: pointer;
  margin-left: 10px;
}

.title {
  color: black;
  font-size: 24px;
  margin: 10px 20px;
}

.menu-button {
  background-color: transparent;
  border: none;
  color: black;
  font-size: 18px;
  cursor: pointer;
  margin-left: auto; /* 将菜单按钮推到右侧 */
}

.theme-toggle {
  background-color: transparent;
  border: none;
  color: black;
  font-size: 24px;
  cursor: pointer;
}

.material-icons {
  font-size: 24px; /* 设置图标的大小 */
}

/* 桌面端 Header 样式 */
.desktop-header-content {
  display: flex;
  align-items: center;
  width: 100%; /* 占满整个 Header 宽度 */
  justify-content: space-between; /* 左右两侧对齐 */
}

.header-nav {
  margin-right: 20px; /* 设置右侧间距 */
  gap: 20px; /* 设置导航链接之间的间距 */
  display: flex; /* 水平排列 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.header-nav .nav-link,
.header-nav .new-button {
  color: black; /* 设置文字颜色为黑色 [[7]] */
  text-decoration: none; /* 去掉下划线 */
  font-size: 16px;
  cursor: pointer; /* 显示手型光标 */
  background-color: transparent; /* 设置背景颜色为透明 */
  border: none; /* 去掉边框 */
  padding: 0;
}

.header-nav .nav-link:hover,
.header-nav .new-button:hover {
  text-decoration: underline; /* 鼠标悬停时添加下划线 */
}

.mobile-header-content {
  width: 100%; /* 占满整个 Header 宽度 */
}

/* 下拉菜单样式 */
.dropdown-menu {
  margin-top: 20px; /* 下拉菜单距离按钮的距离 */
  width: 100%; /* 占满整个 Header 宽度 */
  display: flex; /* 展开时显示 */
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 居中对齐 */
  border-top: 2px solid #f0f0f0; /* 上边框颜色 */
  gap: 10px; /* 设置下拉菜单项之间的间距 */
}

.dropdown-menu .nav-link,
.dropdown-menu .new-button {
  padding: 10px;
  color: black;
  text-align: center;
  background-color: transparent; /* 设置背景颜色为透明 */
  border: none; /* 去掉边框 */
  padding: 0;
  font-size: medium;
}

.dropdown-menu .nav-link:hover,
.dropdown-menu .new-button:hover {
  color: #42b983; /* 鼠标悬停时改变颜色 */
}

body.dark-mode .title {
  color: #a9a9b3;
}

body.dark-mode .app-header {
  background-color: #252627;
}

body.dark-mode .header-nav .nav-link,
body.dark-mode .header-nav .new-button,
body.dark-mode .theme-toggle {
  color: #a9a9b3;
}

body.dark-mode .dropdown-menu .nav-link,
body.dark-mode .dropdown-menu .new-button,
body.dark-mode .menu-button {
  color: #a9a9b3;
}
body.dark-mode .dropdown-menu {
  border-top: 2px solid #3a3b3d; /* 夜间模式下的上边框颜色 */
}

.slug-preview {
  margin-top: 5px;
  color: #666;
  font-size: 12px;
}

body.dark-mode .slug-preview {
  color: #b0b0b0;
}
</style>
