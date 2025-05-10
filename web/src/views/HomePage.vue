<template>
  <div class="home">
    <!-- 浮动窗口 -->
    <el-dialog v-model="dialogVisible" title="新增影片" width="30%">
      <el-form :model="formData" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="formData.title" placeholder="请输入影片标题"></el-input>
        </el-form-item>
        <el-form-item label="演员">
          <el-input v-model="formData.actors" placeholder="请输入演员，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="formData.tags" placeholder="请输入标签，用逗号分隔"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="formData.description"
            type="textarea"
            placeholder="请输入影片简介"
          ></el-input>
        </el-form-item>
        <!-- <el-form-item label="封面">
          <el-input v-model="formData.cover" placeholder="请输入封面图片路径"></el-input>
        </el-form-item> -->
        <el-form-item label="order">
          <el-input v-model="formData.order" placeholder="请输入影片顺序"></el-input>
        </el-form-item>
        <el-form-item label="rating">
          <el-input v-model="formData.rating" placeholder="请输入影片评分"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMovie">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 浮动窗口 -->
    <el-dialog v-model="actorDialogVisible" title="新增演员" width="30%">
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
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="actorDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveActor">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 影片视图 -->
    <div v-if="viewStore.isMovieView" class="movie-view">
      <!-- 新建按钮 -->
      <button class="new-button material-icons" @click="openDialog" title="添加影片">add</button>
      <button @click="saveRanking" class="save-button material-icons" title="保存">save</button>
      <!-- 筛选器 -->
      <div class="filter-container">
        <div class="actor-filter">
          <label for="actor-filter">按演员筛选：</label>
          <el-select
            v-model="selectedActors"
            multiple
            clearable
            filterable
            placeholder="请选择演员"
            style="width: 150px"
            @change="filterMovies"
          >
            <el-option
              v-for="actor in actors"
              :key="actor.name"
              :label="actor.name"
              :value="actor.name"
            ></el-option>
          </el-select>
        </div>

        <div class="rating-filter">
          <label for="rating-filter">按评分筛选：</label>
          <el-slider
            v-model="ratingRange"
            range
            :min="0"
            :max="5"
            :step="1"
            style="width: 100px"
            @change="filterMovies"
          ></el-slider>
          <span style="margin-left: 20px;">{{ ratingRange[0] }} - {{ ratingRange[1] }}</span>
        </div>
      </div>

      <div v-for="(movie, index) in filteredMovies" :key="movie.id" class="movie-item">
        <!-- 封面 -->
        <div class="cover-wrapper" @click="goToDetail(movie.id)">
          <img :src="movie.cover" alt="封面" class="cover" @error="setDefaultCover($event)" />
        </div>
        <!-- 详细信息 -->
        <div class="details">
          <h2>{{ movie.title }}</h2>
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
            <span v-for="i in 5" :key="i" class="star" @click="setRating(movie, i)">
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
              >
                {{ tag }}
              </el-tag>
            </span>
            <span v-else>暂无标签信息</span>
          </p>
          <p><strong>简介：</strong>{{ movie.description }}</p>
        </div>
        <!-- 上移/下移按钮 -->
        <div class="controls">
          <button @click="moveUp(index)" :disabled="index === 0" class="icon-button">
            <el-icon><ArrowUp /></el-icon>
          </button>
          <button
            @click="moveDown(index)"
            :disabled="index === movies.length - 1"
            class="icon-button"
          >
            <el-icon><ArrowDown /></el-icon>
          </button>
        </div>
      </div>
    </div>

    <!-- 演员视图 -->
    <div v-else class="actor-view">
      <!-- 新建按钮 -->
      <button class="new-button material-icons" @click="openActorDialog" title="添加演员">
        add
      </button>
      <h1>演员列表</h1>
      <div class="actor-grid">
        <div v-for="(actor, index) in actors" :key="actor.name" class="actor-item">
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
  </div>
</template>

<script>
// 导入默认图片
import defaultCover from '@/assets/missing.png'
// 导入 Element Plus 图标
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

import axios from 'axios'
import { useViewStore } from '../store/view'

export default {
  name: 'HomePage',
  components: {
    ArrowUp,
    ArrowDown,
  },
  setup() {
    const viewStore = useViewStore()
    return { viewStore }
  },
  data() {
    return {
      movies: [], // 初始为空数组，稍后加载数据
      filteredMovies: [], // 筛选后的影片
      selectedActors: [], // 当前选择的演员
      ratingRange: [0, 5], // 默认评分区间
      defaultCover, // 默认图片路径
      dialogVisible: false, // 控制浮动窗口的显示状态
      actors: [], // 演员列表
      formData: {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 1, // 新增顺序字段
        rating: 0, // 新增评分字段
      },
      actorDialogVisible: false, // 控制浮动窗口的显示状态
      actorFormData: {
        name: '',
        birth: '',
        debut: '',
      },
    }
  },
  methods: {
    openDialog() {
      this.dialogVisible = true // 打开浮动窗口 [[4]]
    },
    setRating(movie, rating) {
      movie.rating = rating // 更新当前影片的评分
    },
    async saveMovie() {
      try {
        const response = await axios.post('/api/create-movie', this.formData)
        if (response.data.success) {
          this.$message.success('影片已成功创建！')
          this.dialogVisible = false // 关闭浮动窗口
          this.resetForm() // 清空表单
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
    resetForm() {
      this.formData = {
        title: '',
        actors: '',
        tags: '',
        description: '',
        order: 1,
      }
    },
    openActorDialog() {
      this.actorDialogVisible = true // 打开浮动窗口 [[1]]
    },
    async saveActor() {
      try {
        const response = await axios.post('/api/create-actor', this.actorFormData)
        if (response.data.success) {
          this.$message.success('演员已成功创建！')
          this.actorDialogVisible = false // 关闭浮动窗口
          this.resetActorForm() // 清空表单
        } else {
          this.$message.error('创建失败，请稍后再试！')
        }
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message)
        this.$message.error('创建失败，请稍后再试！')
      }
    },
    resetActorForm() {
      this.actorFormData = {
        name: '',
        birth: '',
        debut: '',
      }
    },
    moveUp(index) {
      if (index > 0) {
        const temp = this.movies[index]
        this.movies.splice(index, 1)
        this.movies.splice(index - 1, 0, temp)
      }
    },
    moveDown(index) {
      if (index < this.movies.length - 1) {
        const temp = this.movies[index]
        this.movies.splice(index, 1)
        this.movies.splice(index + 1, 0, temp)
      }
    },
    setDefaultCover(event) {
      event.target.src = this.defaultCover // 设置为默认图片路径
    },
    goToDetail(id) {
      console.log('跳转到详情页，电影 ID:', id) // 调试信息
      // 使用 Vue Router 跳转到详情页
      this.$router.push({ name: 'MovieDetail', params: { id } }) // 跳转到详情页
    },
    goToHome() {
      this.$router.push({ name: 'HomePage' }) // 返回主页 [[6]]
    },
    goToActor(name) {
      console.log('跳转到演员详情页，演员姓名:', name) // 调试信息
      this.$router.push({ name: 'ActorDetail', params: { name } }) // 跳转到演员详情页
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
    filterMovies() {
      let filtered = [...this.movies]
      if (this.selectedActors.length > 0) {
        this.filteredMovies = this.movies.filter((movie) =>
          this.selectedActors.some(
            (actor) => movie.actors && movie.actors.split(', ').includes(actor),
          ),
        )
      } else {
        this.filteredMovies = [...this.movies] // 如果未选择演员，则显示所有影片
      }

      // 再根据评分区间筛选
      if (this.ratingRange[0] >= 0 || this.ratingRange[1] <= 5) {
        filtered = this.filteredMovies.filter(
          (movie) => movie.rating >= this.ratingRange[0] && movie.rating <= this.ratingRange[1],
        )
      }

      this.filteredMovies = filtered
    },
    async saveRanking() {
      const newRanking = this.movies.map((movie, index) => ({
        id: movie.id,
        order: index + 1, // 更新顺序值
        rating: movie.rating || 0, // 如果没有评分，默认为 0
      }))
      try {
        await axios.post('/api/update-ranking', { ranking: newRanking })
        this.$message.success('排行已更新！')
      } catch (error) {
        this.$message.error('更新失败，请稍后再试！')
      }
    },
  },
  async created() {
    try {
      const response = await axios.get('/api/movies')
      this.movies = response.data
      this.filteredMovies = response.data // 初始化筛选后的影片
    } catch (error) {
      console.error('Error fetching movies:', error)
    }

    try {
      const response = await axios.get('/api/actors')
      this.actors = response.data
    } catch (error) {
      console.error('Error fetching actors:', error)
    }
  },
}
</script>

<style scoped>
.logo img {
  width: 50px;
  cursor: pointer;
}

.actor-tag {
  margin-right: 5px;
  cursor: pointer;
}

.tag-item {
  margin-right: 5px;
}

.home {
  font-family: Arial, sans-serif;
  align-items: center;
}

.actor-cover {
  max-width: 200px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 10%; /* 圆形封面 */
}

.actor-item {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 居中对齐 */
  text-align: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 不设置固定高度，让内容决定高度 */
}

.actor-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  word-wrap: break-word; /* 长名字自动换行 */
}

.actor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 40px;
  margin-top: 20px;
}

.actor-view {
  max-width: 1200px;
  justify-content: center; /* 水平居中 */
  margin: auto;
}

.movie-view {
  max-width: 800px;
  justify-content: center; /* 水平居中 */
  margin: auto;
}

.movie-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

/* 宽屏设备：横向排列 */
@media (min-width: 768px) {
  .movie-item {
    flex-direction: row; /* 横向排列 */
  }
  .cover {
    max-width: 350px; /* 设置最大宽度，避免图片过大 */
    object-fit: cover; /* 确保图片填充整个区域，避免拉伸或变形 */
    aspect-ratio: 16 / 9; /* 设置宽高比为 16:9 */
    margin-right: 20px;
  }
  .details {
    flex: 1;
    text-align: left;
  }
  .controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
}

/* 窄屏设备：竖向排列 */
@media (max-width: 768px) {
  .movie-item {
    flex-direction: column; /* 竖向排列 */
    align-items: flex-start; /* 左对齐 */
  }
  .cover {
    max-width: 100%; /* 让封面占满容器宽度 */
    margin-right: 0; /* 移除右侧间距 */
    margin-bottom: 10px; /* 添加底部间距 */
  }
  .details {
    width: 100%; /* 占满容器宽度 */
    text-align: left;
  }
  .controls {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
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

.star:hover {
  cursor: pointer; /* 鼠标悬停时显示为手型 */
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #409eff;
}

.icon-button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.save-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
.save-button:hover {
  background-color: #33a07c;
}

.new-button {
  margin: 20px 10px;
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.filter-container {
  margin-bottom: 20px;
  align-items: left;
  display: flex;
  flex-direction: column;
}
.filter-container label {
  margin-right: 10px;
}
.filter-container select {
  margin-left: 10px;
}

.rating-filter {
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-left: 0;
}

.rating-filter span {
  margin-left: 10px;
}
</style>
