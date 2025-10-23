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
        <!-- 导航图标区域 -->
        <div class="nav-icons">
          <span @click="goToMovies" class="nav-icon" title="影片排行页面">
            <span class="material-icons">movie</span>
          </span>
          <span @click="goToActors" class="nav-icon" title="演员列表页面">
            <span class="material-icons">people</span>
          </span>
          <span @click="goToTags" class="nav-icon" title="标签页页面">
            <span class="material-icons">local_offer</span>
          </span>
          <span @click="goToPosts" class="nav-icon" title="博客列表页面">
            <span class="material-icons">article</span>
          </span>
          <span @click="goToImgbed" class="nav-icon" title="图床管理页面">
            <span class="material-icons">collections</span>
          </span>
        </div>

        <!-- 操作区域 -->
        <div class="action-area">
          <!-- 新建下拉菜单 -->
          <div class="create-dropdown" @click="toggleCreateMenu">
            <button class="create-button">
              <span class="material-icons">add</span>
              <span class="create-text">新建</span>
              <span class="material-icons dropdown-arrow">{{
                isCreateMenuOpen ? 'expand_less' : 'expand_more'
              }}</span>
            </button>
            <div v-if="isCreateMenuOpen" class="create-menu">
              <div @click="openMovieDialog" class="create-menu-item">
                <span class="material-icons">movie</span>
                <span>新增影片</span>
              </div>
              <div @click="openActorDialog" class="create-menu-item">
                <span class="material-icons">person_add</span>
                <span>新增演员</span>
              </div>
              <div @click="openPostDialog" class="create-menu-item">
                <span class="material-icons">post_add</span>
                <span>新建博客</span>
              </div>
              <div @click="openImageDialog" class="create-menu-item">
                <span class="material-icons">image</span>
                <span>上传图片</span>
              </div>
            </div>
          </div>

          <!-- 主题样式切换器 -->
          <ThemeSwitcher />

          <!-- 暗色模式切换 -->
          <button class="theme-toggle" @click="toggleTheme" title="切换暗色/亮色模式">
            <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
          </button>
        </div>
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
        <!-- 导航图标区域 -->
        <div class="nav-icons-mobile">
          <span @click="goToMovies" class="nav-icon" title="影片排行页面">
            <span class="material-icons">movie</span>
            <span class="nav-text">影片排行</span>
          </span>
          <span @click="goToActors" class="nav-icon" title="演员列表页面">
            <span class="material-icons">people</span>
            <span class="nav-text">演员列表</span>
          </span>
          <span @click="goToTags" class="nav-icon" title="标签页页面">
            <span class="material-icons">local_offer</span>
            <span class="nav-text">标签列表</span>
          </span>
          <span @click="goToPosts" class="nav-icon" title="博客列表页面">
            <span class="material-icons">article</span>
            <span class="nav-text">博客列表</span>
          </span>
          <span @click="goToImgbed" class="nav-icon" title="图床管理页面">
            <span class="material-icons">collections</span>
            <span class="nav-text">图床管理</span>
          </span>
        </div>

        <!-- 操作区域 -->
        <div class="action-area-mobile">
          <button class="new-button" @click="openMovieDialog" title="新增影片">
            <span class="material-icons">movie</span>
            <span class="button-text">新增影片</span>
          </button>
          <button class="new-button" @click="openActorDialog" title="新增演员">
            <span class="material-icons">person_add</span>
            <span class="button-text">新增演员</span>
          </button>
          <button class="new-button" @click="openPostDialog" title="新建博客">
            <span class="material-icons">post_add</span>
            <span class="button-text">新建博客</span>
          </button>
          <button class="new-button" @click="openImageDialog" title="上传图片">
            <span class="material-icons">image</span>
            <span class="button-text">上传图片</span>
          </button>
        </div>
        <div class="theme-toggle-mobile">
          <button class="theme-toggle" @click="toggleTheme">
            <span class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 上传图片浮动窗口 -->
    <el-dialog v-model="imageDialogVisible" title="上传图片" width="80%">
      <el-form :model="imageFormData" label-width="80px">
        <el-form-item label="图片类型">
          <el-select
            v-model="imageFormData.type"
            placeholder="请选择图片类型"
            style="width: 100%"
            @change="handleImageTypeChange"
          >
            <el-option label="演员" value="actor"></el-option>
            <el-option label="影片" value="movie"></el-option>
            <el-option label="博客" value="post"></el-option>
            <el-option label="图床" value="imgbed"></el-option>
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
        <el-form-item label="图片名称">
          <el-input
            v-model="imageFormData.name"
            :placeholder="getImageNamePlaceholder()"
          ></el-input>
          <div v-if="imageFormData.type === 'imgbed' && selectedImageFile" class="filename-preview">
            <small
              >{{ imageFormData.name ? '文件名: ' + imageFormData.name : '文件名: ' + getOriginalFileName()
              }}{{ getFileExtension() }}</small
            >
          </div>
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
          <el-select
            v-model="movieFormData.selectedActors"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择演员或输入新演员名称"
            style="width: 100%"
            @change="handleActorSelection"
          >
            <el-option
              v-for="actor in availableActors"
              :key="actor.name"
              :label="actor.name"
              :value="actor.name"
            />
          </el-select>
          <div v-if="movieFormData.selectedActors.length > 0" class="selected-actors">
            <small>已选择: {{ movieFormData.selectedActors.join(', ') }}</small>
          </div>
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
        <el-form-item label="喜爱度">
          <el-input-number
            v-model="actorFormData.favorite"
            :min="1"
            :max="5"
            :precision="0"
            placeholder="请输入喜爱度(1-5)"
          ></el-input-number>
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
import { useThemeStore } from '../store/theme'
import axios from 'axios'
import { UploadFilled } from '@element-plus/icons-vue'
import ThemeSwitcher from './ThemeSwitcher.vue'

export default {
  name: 'AppHeader',
  components: {
    ThemeSwitcher,
    UploadFilled,
  },
  data() {
    return {
      isMobile: false, // 是否显示菜单按钮
      isMenuOpen: false, // 菜单是否展开
      isDarkMode: false, // 是否启用夜间模式（从 themeStore 同步）
      movieDialogVisible: false, // 控制浮动窗口的显示状态
      movieFormData: {
        title: '',
        actors: '',
        selectedActors: [],
        tags: '',
        description: '',
        order: 10,
        rating: 0,
      },
      availableActors: [], // 可选择的演员列表
      actorDialogVisible: false, // 控制浮动窗口的显示状态
      actorFormData: {
        name: '',
        birth: '',
        debut: '',
        favorite: 1,
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
        date: '',
      },
      isCreateMenuOpen: false, // 控制新建操作下拉菜单的显示状态
    }
  },
  setup() {
    const viewStore = useViewStore()
    const themeStore = useThemeStore()
    return { viewStore, themeStore }
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
    goToImgbed() {
      // 在新窗口打开图床管理页面
      const route = this.$router.resolve({ name: 'ImgbedPage' })
      window.open(route.href, '_blank')
      this.isMenuOpen = false // 关闭菜单
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen // 切换菜单状态
    },
    toggleTheme() {
      this.themeStore.toggleDarkMode() // 使用 themeStore 切换暗色模式
      this.isDarkMode = this.themeStore.darkMode // 同步本地状态
    },
    toggleCreateMenu() {
      this.isCreateMenuOpen = !this.isCreateMenuOpen
    },
    handleClickOutside(event) {
      // 检查点击是否在新建下拉菜单外部
      const createDropdown = event.target.closest('.create-dropdown')
      if (!createDropdown && this.isCreateMenuOpen) {
        this.isCreateMenuOpen = false
      }
    },
    checkScreenWidth() {
      this.isMobile = window.innerWidth < 768 // 当屏幕宽度小于 768px 时显示菜单按钮 [[1]]
    },
    toggleView() {
      this.viewStore.toggleView()
    },
    openMovieDialog() {
      this.movieDialogVisible = true // 打开浮动窗口
      this.fetchAvailableActors() // 获取可选择的演员列表
      this.isCreateMenuOpen = false // 关闭新建菜单
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
        selectedActors: [],
        tags: '',
        description: '',
        order: 1,
        rating: 0,
      }
      this.movieImageFileList = []
      this.selectedMovieImageFile = null
    },
    async fetchAvailableActors() {
      try {
        const response = await axios.get('/api/actors')
        this.availableActors = response.data
      } catch (error) {
        console.error('Error fetching actors:', error)
        this.availableActors = []
      }
    },
    handleActorSelection(selectedActors) {
      // 将选中的演员名称转换为逗号分隔的字符串
      this.movieFormData.actors = selectedActors.join(', ')
    },
    openActorDialog() {
      this.actorDialogVisible = true
      this.isCreateMenuOpen = false // 关闭新建菜单
    },
    resetActorForm() {
      this.actorFormData = {
        name: '',
        birth: '',
        debut: '',
        favorite: 1,
      }
      this.actorImageFileList = []
      this.selectedActorImageFile = null
    },
    openImageDialog() {
      this.imageDialogVisible = true
      this.isCreateMenuOpen = false // 关闭新建菜单
    },
    openPostDialog() {
      this.postDialogVisible = true
      this.isCreateMenuOpen = false // 关闭新建菜单
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
      // 如果是图床类型且名称为空，自动填充原始文件名
      if (this.imageFormData.type === 'imgbed' && !this.imageFormData.name.trim()) {
        this.imageFormData.name = this.getOriginalFileName()
      }
    },
    handleImageTypeChange() {
      // 当切换到图床类型时，如果已选择文件且名称为空，自动填充原始文件名
      if (
        this.imageFormData.type === 'imgbed' &&
        this.selectedImageFile &&
        !this.imageFormData.name.trim()
      ) {
        this.imageFormData.name = this.getOriginalFileName()
      }
    },
    getImageNamePlaceholder() {
      if (this.imageFormData.type === 'imgbed') {
        return '请输入图片名称（不含扩展名，留空使用原文件名）'
      }
      return '请输入图片名称（不需要包含文件后缀）'
    },
    getOriginalFileName() {
      if (!this.selectedImageFile) return ''
      const filename = this.selectedImageFile.name
      return filename.substring(0, filename.lastIndexOf('.')) || filename
    },
    getFileExtension() {
      if (!this.selectedImageFile) return ''
      const filename = this.selectedImageFile.name
      const lastDot = filename.lastIndexOf('.')
      return lastDot !== -1 ? filename.substring(lastDot) : ''
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
          // 触发页面刷新事件
          this.$eventBus.emit('movie-created')
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
        formData.append('favorite', this.actorFormData.favorite)

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
          // 触发页面刷新事件
          this.$eventBus.emit('actor-created')
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
      if (!this.imageFormData.type) {
        this.$message.error('请选择图片类型！')
        return
      }
      // 对于非图床类型，必须输入名称
      if (this.imageFormData.type !== 'imgbed' && !this.imageFormData.name.trim()) {
        this.$message.error('请输入图片名称！')
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
          this.$message.success(`图片上传成功！路径: ${response.data.path}`)
          this.imageDialogVisible = false
          this.resetImageForm()
          // 触发页面刷新事件
          this.$eventBus.emit('image-uploaded', { type: this.imageFormData.type })
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
          content: `# ${this.postFormData.title}`,
          date: this.postFormData.date || new Date().toISOString().split('T')[0],
        }

        const response = await axios.post('/api/create-post', postData)

        if (response.data.success) {
          this.$message.success('博客已成功创建！')
          this.postDialogVisible = false
          this.resetPostForm()
          // 触发页面刷新事件
          this.$eventBus.emit('post-created')
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
    // 添加点击外部关闭下拉菜单的监听器
    document.addEventListener('click', this.handleClickOutside)
    // 从 themeStore 同步暗色模式状态
    this.isDarkMode = this.themeStore.darkMode
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenWidth) // 移除监听器
    document.removeEventListener('click', this.handleClickOutside) // 移除点击外部监听器
  },
}
</script>

<style scoped>
.app-header {
  background: var(--primary-gradient);
  padding: 10px 0 0 0;
  align-items: center;
  display: flex;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 1000;
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
  color: white;
  font-size: 24px;
  margin: 10px 20px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.menu-button {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-left: auto;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.menu-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.theme-toggle {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: rotate(15deg);
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

/* 导航图标样式 */
.nav-icons {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.nav-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-icon .material-icons {
  font-size: 24px;
}

/* 操作区域样式 */
.action-area {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 新建下拉菜单样式 */
.create-dropdown {
  position: relative;
}

.create-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.create-button:hover {
  background-color: rgba(255, 255, 255, 0.35);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.create-text {
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 18px !important;
  transition: transform 0.3s ease;
}

.create-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: var(--shadow-md);
  min-width: 160px;
  z-index: 1000;
  overflow: hidden;
}

.create-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: var(--text-primary);
}

.create-menu-item:hover {
  background-color: var(--bg-secondary);
}

.create-menu-item .material-icons {
  font-size: 20px;
  color: var(--text-tertiary);
}

/* 移动端样式 */
.nav-icons-mobile {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  align-items: center;
}

.nav-icons-mobile .nav-icon {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
  width: 100%;
  box-sizing: border-box;
  height: 48px;
}

.nav-icons-mobile .nav-icon:hover {
  background-color: var(--bg-secondary);
  transform: translateY(-2px);
}

.nav-icons-mobile .nav-icon .material-icons {
  font-size: 20px;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.action-area-mobile {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid var(--border-light);
  border-bottom: 1px solid var(--border-light);
  width: 100%;
}

.action-area-mobile .new-button {
  background-color: #42b983;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
  color: white;
  border: none;
  font-size: 14px;
  height: 48px;
}

.action-area-mobile .new-button:hover {
  background-color: #3aa876;
  transform: translateY(-2px);
}

.action-area-mobile .new-button .material-icons {
  font-size: 20px;
}

.button-text {
  font-weight: 500;
  font-size: 14px;
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
  border-top: 2px solid var(--border-light); /* 上边框颜色 */
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

/* Dark mode styles are now handled by CSS variables */

.slug-preview {
  margin-top: 5px;
  color: var(--text-tertiary);
  font-size: 12px;
}

.selected-actors {
  margin-top: 5px;
  color: var(--text-tertiary);
  font-size: 12px;
}

.filename-preview {
  margin-top: 5px;
  color: var(--text-tertiary);
  font-size: 12px;
}
</style>
