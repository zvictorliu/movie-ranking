<template>
  <div class="home">
    <div v-for="(movie, index) in movies" :key="movie.id" class="movie-item">
      <!-- 封面 -->
      <div class="cover-wrapper" @click="goToDetail(movie.id)">
        <img
          :src="movie.cover"
          alt="封面"
          class="cover"
          @error="setDefaultCover($event)"
        />
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
        <button
          @click="moveUp(index)"
          :disabled="index === 0"
          class="icon-button"
        >
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
</template>

<script>
// 导入默认图片
import defaultCover from "@/assets/missing.png";
// 导入 Element Plus 图标
import { ArrowUp, ArrowDown } from "@element-plus/icons-vue";

import axios from "axios";

export default {
  name: "HomePage",
  components: {
    ArrowUp,
    ArrowDown,
  },
  data() {
    return {
      movies: [], // 初始为空数组，稍后加载数据
      defaultCover, // 默认图片路径
    };
  },
  methods: {
    moveUp(index) {
      if (index > 0) {
        const temp = this.movies[index];
        this.movies.splice(index, 1);
        this.movies.splice(index - 1, 0, temp);
      }
    },
    moveDown(index) {
      if (index < this.movies.length - 1) {
        const temp = this.movies[index];
        this.movies.splice(index, 1);
        this.movies.splice(index + 1, 0, temp);
      }
    },
    setDefaultCover(event) {
      event.target.src = this.defaultCover; // 设置为默认图片路径
    },
    goToDetail(id) {
      console.log("跳转到详情页，电影 ID:", id); // 调试信息
      // 使用 Vue Router 跳转到详情页
      this.$router.push({ name: "MovieDetail", params: { id } }); // 跳转到详情页
    },
    goToHome() {
      this.$router.push({ name: "HomePage" }); // 返回主页 [[6]]
    },
    goToActor(name) {
      console.log("跳转到演员详情页，演员姓名:", name); // 调试信息
      this.$router.push({ name: "ActorDetail", params: { name } }); // 跳转到演员详情页
    },
    getActorTagType(actorName) {
      // 根据演员名字生成固定的类型映射 [[6]]
      const types = ["success", "info", "warning", "danger"];
      const typeIndex = Math.abs(this.hashCode(actorName)) % types.length;
      return types[typeIndex];
    },
    getTagType(tag) {
      // 根据标签名字生成固定的类型映射 [[6]]
      const types = ["success", "info", "warning", "danger"];
      const typeIndex = Math.abs(this.hashCode(tag)) % types.length;
      return types[typeIndex];
    },
    hashCode(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      return hash;
    },
  },
  async created() {
    try {
      const response = await axios.get("http://localhost:5000/api/movies"); // 调用后端 API [[2]]
      this.movies = response.data;
    } catch (error) {
      console.error("请求失败:", error);
    }
  },
};
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
  padding-left: 20%;
  padding-right: 20%;
}
.movie-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}
.cover {
  max-width: 200px; /* 设置最大宽度，避免图片过大 [[8]] */
  object-fit: cover; /* 确保图片填充整个区域，避免拉伸或变形 [[5]] */
  aspect-ratio: 16 / 9; /* 设置宽高比为 16:9 [[2]] */
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


</style>
