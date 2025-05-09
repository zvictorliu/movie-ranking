<template>
  <div class="actor-detail">
    <h1>{{ actor.name }}</h1>
    <img
      :src="actor.cover"
      alt="演员封面"
      class="cover"
      @error="setDefaultCover($event)"
    />
    <p><strong>出生日期：</strong>{{ actor.birth }}</p>
    <p><strong>出道日期：</strong>{{ actor.debut }}</p>

    <!-- 显示 Markdown 正文 -->
    <div v-html="actor.body_html" class="content"></div>

    <!-- 返回按钮 -->
    <button @click="goBack">返回</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ActorDetailPage",
  data() {
    return {
      actor: {},
    };
  },
  async created() {
    const { name } = this.$route.params;
    try {
      const response = await axios.get(
        `/api/actor/${name}`
      );
      this.actor = response.data;
      console.log("演员详情:", this.actor); // 调试信息
    } catch (error) {
      console.error("请求失败:", error);
    }
  },
  methods: {
    setDefaultCover(event) {
      event.target.src = "/imgs/default.jpg";
    },
    goBack() {
      this.$router.go(-1); // 返回上一页 [[7]]
    },
  },
};
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

.cover {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
}

.content ::v-deep(img) { /* 深度选择器，确保样式应用于子组件的 img 元素 */
  max-width: 100%; /* 确保图片宽度不超过父容器 */
  height: auto; /* 保持图片比例 */
  border-radius: 10px; /* 添加圆角效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 [[8]] */
}


button {
  padding: 10px 20px;
  cursor: pointer;
  position: relative;
}
</style>
