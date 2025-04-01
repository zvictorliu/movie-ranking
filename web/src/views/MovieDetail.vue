<template>
  <div class="movie-detail">
    <h1>{{ movie.title }}</h1>
    <img
      :src="movie.cover"
      alt="封面"
      class="cover"
      @error="setDefaultCover($event)"
    />
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

    <!-- 显示 Markdown 正文 -->
    <div v-html="movie.body_html" class="content"></div>

    <!-- 上一页、下一页按钮 -->
    <div class="navigation">
      <button @click="navigate(-1)" :disabled="!prevMovie">上一页</button>
      <button @click="navigate(1)" :disabled="!nextMovie">下一页</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MovieDetail",
  data() {
    return {
      movie: {},
      prevMovie: null,
      nextMovie: null,
    };
  },
  async created() {
    const { id } = this.$route.params;
    const allMovies = await this.fetchMovies();
    const currentIndex = allMovies.findIndex((m) => m.id === id);

    if (currentIndex !== -1) {
      this.movie = allMovies[currentIndex];
      this.prevMovie = currentIndex > 0 ? allMovies[currentIndex - 1] : null;
      this.nextMovie =
        currentIndex < allMovies.length - 1
          ? allMovies[currentIndex + 1]
          : null;
    }
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get("http://localhost:5000/api/movies"); // 调用后端 API [[2]]
        return response.data; // 返回电影列表
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
    setDefaultCover(event) {
      event.target.src = "/imgs/default.jpg"; // 默认图片路径
    },
    navigate(direction) {
      const targetMovie = direction === -1 ? this.prevMovie : this.nextMovie;
      if (targetMovie) {
        this.$router.push({
          name: "MovieDetail",
          params: { id: targetMovie.id },
        });
      }
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
};
</script>

<style scoped>
.logo img {
  width: 100px;
  cursor: pointer;
}
.movie-detail {
  padding-left: 20%;
  padding-right: 20%;
}

.actor-tag {
  margin-right: 5px;
  cursor: pointer;
}

.tag-item {
  margin-right: 5px;
}

.cover {
  max-width: 60%;
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
</style>
